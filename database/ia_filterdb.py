        return []

    if USE_CAPTION_FILTER:
        filter = {'$or': [{'file_name': regex}, {'caption': regex}]}
    else:
        filter = {'file_name': regex}

    if file_type:
        filter['file_type'] = file_type

    total_results = await Media.count_documents(filter)
    next_offset = offset + max_results

    if next_offset > total_results:
        next_offset = ''

    cursor = Media.find(filter)
    # Sort by recent
    cursor.sort('$natural', -1)
    # Slice files according to offset and max results
    cursor.skip(offset).limit(max_results)
    # Get list of files
    files = await cursor.to_list(length=max_results)

    # Present cleaner names and keep series seasons together. This modifies
    # only the returned in-memory documents, never the MongoDB records.
    for file in files:
        original_name = file['file_name']
        for banned_word in banned_words:
            pattern = re.compile(re.escape(banned_word), re.IGNORECASE)
            original_name = pattern.sub('', original_name).strip()
        file['file_name'] = clean_search_result_name(original_name, query)

    files.sort(key=lambda item: _result_sort_key(item, query))
    return files, next_offset, total_results

async def get_all_files():
    cursor = Media.find() 
    all_files = await cursor.to_list(length=10000)  
    return [file['file_name'] for file in all_files]

async def get_bad_files(query, file_type=None, filter=False):
    """For given query return (results, next_offset)"""
    query = query.strip()
    #if filter:
        #better ?
        #query = query.replace(' ', r'(\s|\.|\+|\-|_)')
        #raw_pattern = r'(\s|_|\-|\.|\+)' + query + r'(\s|_|\-|\.|\+)'
    if not query:
        raw_pattern = '.'
    elif ' ' not in query:
        raw_pattern = r'(\b|[\.\+\-_])' + query + r'(\b|[\.\+\-_])'
    else:
        raw_pattern = query.replace(' ', r'.*[\s\.\+\-_]')
    
    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except:
        return []

    if USE_CAPTION_FILTER:
        filter = {'$or': [{'file_name': regex}, {'caption': regex}]}
    else:
        filter = {'file_name': regex}

    if file_type:
        filter['file_type'] = file_type

    total_results = await Media.count_documents(filter)

    cursor = Media.find(filter)
    # Sort by recent
    cursor.sort('$natural', -1)
    # Get list of files
    files = await cursor.to_list(length=total_results)

    return files, total_results

async def get_file_details(query):
    try:
        banned_words = script.BLACKLIST
        filter = {'file_id': query}
        cursor = Media.find(filter)
        filedetails = await cursor.to_list(length=1)
        if filedetails:
            file = filedetails[0]
            original_file_name = getattr(file, 'file_name', '')
            modified_file_name = original_file_name
            for banned_word in banned_words:
                pattern = re.compile(re.escape(banned_word), re.IGNORECASE)
                modified_file_name = pattern.sub('', modified_file_name).strip()
            if not modified_file_name:
                modified_file_name = "DefaultFileName"
            setattr(file, 'file_name', modified_file_name)
        return filedetails
    except Exception as e:
        logging.error("An error occurred:", exc_info=True)
        return None

def encode_file_id(s: bytes) -> str:
    r = b""
    n = 0

    for i in s + bytes([22]) + bytes([4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0

            r += bytes([i])

    return base64.urlsafe_b64encode(r).decode().rstrip("=")


def encode_file_ref(file_ref: bytes) -> str:
    return base64.urlsafe_b64encode(file_ref).decode().rstrip("=")


def unpack_new_file_id(new_file_id):
    """Return file_id, file_ref"""
    decoded = FileId.decode(new_file_id)
    file_id = encode_file_id(
        pack(
            "<iiqq",
            int(decoded.file_type),
            decoded.dc_id,
            decoded.media_id,
            decoded.access_hash
        )
    )
    file_ref = encode_file_ref(decoded.file_reference)
    return file_id, file_ref
