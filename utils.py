# This code has been modified by @Looteredev
# Please do not remove this credit
import logging
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid, ChatAdminRequired, MessageIdInvalid, EmoticonInvalid, ReactionInvalid
from info import *
from imdb import Cinemagoer 
import asyncio
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import enums
from typing import Union
from Script import script
import pytz
import random 
from random import choice
from asyncio import sleep
import time
import re
import os
from datetime import datetime, timedelta, date, time
import string
from typing import List
from database.users_chats_db import db
from bs4 import BeautifulSoup
import requests
import aiohttp
from shortzy import Shortzy

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

BTN_URL_REGEX = re.compile(
    r"(\[([^\[]+?)\]\((buttonurl|buttonalert):(?:/{0,2})(.+?)(:same)?\))"
)

try:
    imdb = Cinemagoer('http')
except Exception:
    try:
        imdb = Cinemagoer()
    except Exception as e:
        logger.error(f"Failed to initialize Cinemagoer: {e}")
        imdb = None

BANNED = {}
SMART_OPEN = '“'
SMART_CLOSE = '”'
START_CHAR = ('\'', '"', SMART_OPEN)

# temp db for banned 
class temp(object):
    BANNED_USERS = []
    BANNED_CHATS = []
    ME = None
    CURRENT=int(os.environ.get("SKIP", 2))
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None
    SETTINGS = {}
    KEYWORD = {}
    GETALL = {}
    SPELL_CHECK = {}
    IMDB_CAP = {}
    CHAT = {}

def clean_file_name(file_name: str, max_len: int = 55) -> str:
    """
    Clean display-only noise from filenames while preserving the original metadata.
    Hides uploader/channel prefixes, website domains, @usernames, and messy punctuation.
    """
    if not file_name:
        return 'File'
    
    raw = str(file_name).strip()
    # 1. Strip common media file extensions
    cleaned = re.sub(r'\.(mkv|mp4|avi|mov|wmv|webm|zip|rar|tar|iso|flv|m4v|ts|3gp)$', '', raw, flags=re.IGNORECASE)
    
    # 2. Remove leading brackets like [TG @channel], [MoviesFlix.in], {MoviesNation}, (VegaMovies)
    cleaned = re.sub(r'^[\[\(\{][^\]\)\}]+?[\]\)\}]\s*[\-:\s_]*', '', cleaned)
    cleaned = re.sub(r'^[\[\(\{][^\]\)\}]+?[\]\)\}]\s*[\-:\s_]*', '', cleaned)
    
    # 3. Remove leading pipe tags: e.g. | MkvCinemas |
    cleaned = re.sub(r'^[\|\s]+[^\|]+?[\|\s]+\s*', '', cleaned)
    
    # 4. Remove leading @username (e.g. @rkmovieszip_ or @Looteredev_)
    cleaned = re.sub(r'^@[a-zA-Z0-9_]{3,32}?(?:[_\s\.\-:]+|$)', '', cleaned)
    
    # 5. Remove leading website/domain: e.g. www.1Tamilmv.men - or MoviesFlix.in - 
    cleaned = re.sub(r'^(?:https?://\S+|www\.\S+|[a-zA-Z0-9_\-]+\.(?:com|org|net|in|me|to|vip|cc|site|xyz|nl|top|co|live|app|link|club|store|men))\s*[\-\:\s_]*', '', cleaned, flags=re.IGNORECASE)
    
    # 6. Remove remaining @usernames inside string
    cleaned = re.sub(r'@[a-zA-Z0-9_]{3,32}', '', cleaned)
    
    # 7. Remove remaining domain links inside string
    cleaned = re.sub(r'\b(?:https?://|www\.)[a-zA-Z0-9\-]+(?:\.[a-zA-Z]{2,})+(?:/\S*)?', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\b[a-zA-Z0-9\-]+(?:\.(?:com|org|net|in|me|to|vip|cc|site|xyz|nl|top|club|link|store|men))\b', '', cleaned, flags=re.IGNORECASE)
    
    # 8. Replace underscores with spaces
    cleaned = cleaned.replace('_', ' ')
    
    # 9. Clean dots while protecting audio channels like 5.1 and 2.0
    cleaned = re.sub(r'(?<=[57])\.(?=1\b)|(?<=[2])\.(?=0\b)', '__DOT__', cleaned)
    cleaned = cleaned.replace('.', ' ')
    cleaned = cleaned.replace('__DOT__', '.')
    
    # 10. Remove empty brackets
    cleaned = re.sub(r'\[\s*\]|\(\s*\)|\{\s*\}', '', cleaned)
    
    # 11. Normalize spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip(' -_:|')
    
    # Fallback if over-stripped
    if not cleaned:
        cleaned = re.sub(r'\.(mkv|mp4|avi|mov|wmv|webm|zip|rar|tar|iso|flv|m4v|ts|3gp)$', '', raw, flags=re.IGNORECASE).strip()
    if not cleaned:
        cleaned = raw
        
    # Truncate gracefully if longer than max_len
    if len(cleaned) > max_len:
        cleaned = cleaned[:max_len - 3].strip() + '...'
        
    return cleaned


def extract_season_episode(file_obj):
    """
    Extract (season, is_individual_ep, episode) tuple for season-first natural sorting.
    Packs (complete seasons) get priority 0, individual episodes get priority 1.
    """
    if isinstance(file_obj, str):
        fn = file_obj
    elif isinstance(file_obj, dict):
        fn = file_obj.get('file_name', '')
    else:
        fn = getattr(file_obj, 'file_name', getattr(file_obj, 'name', str(file_obj)))
        
    name = str(fn).upper()
    
    # 1. Match S01E01 / S1E1 / S01 EP01 / S01-01 / Season 1 Episode 1
    se_match = re.search(r'\bS(?:EASON\s*)?(\d{1,2})\s*[-._\s]*E(?:PISODE\s*|P)?\s*(\d{1,3})\b', name)
    if se_match:
        season = int(se_match.group(1))
        episode = int(se_match.group(2))
        return (season, 1, episode)
        
    # 2. Match Complete Season / Season Pack: e.g. Season 1 Complete / S01 Complete / S01-S04 / Complete Season
    is_pack = bool(re.search(r'\b(COMPLETE|ALL\s*EPISODES?|ZIP|BATCH|PACK|COLLECTION)\b', name))
    s_match = re.search(r'\b(?:SEASON|S)\s*(\d{1,2})\b', name)
    if s_match:
        season = int(s_match.group(1))
        return (season, 0, 0)
        
    # 3. Match standalone Episode: e.g. EP 01 / Episode 01
    ep_match = re.search(r'\b(?:EPISODE|EP)\s*(\d{1,3})\b', name)
    if ep_match:
        return (1, 1, int(ep_match.group(1)))
        
    # Non-series files stay grouped
    return (9999, 9999, 9999)


def sort_files_season_first(files):
    """
    Sorts a list of file objects/dicts season-first and preserves natural episode order.
    Non-series files keep their natural relative order.
    """
    if not files:
        return files
    has_series = any(extract_season_episode(f)[0] != 9999 for f in files)
    if not has_series:
        return files
    return sorted(files, key=extract_season_episode)


def extract_year(file_obj):
    """
    Extract 4-digit release year from filename.
    """
    if isinstance(file_obj, str):
        fn = file_obj
    elif isinstance(file_obj, dict):
        fn = file_obj.get('file_name', '')
    else:
        fn = getattr(file_obj, 'file_name', getattr(file_obj, 'name', str(file_obj)))
    m = re.findall(r'\b(19\d\d|20\d\d)\b', str(fn))
    return int(m[-1]) if m else 0


def sort_files(files, sort_by='season'):
    """
    Multi-criteria file sorter for search result UI controls:
    - 'season': Complete Season packs first, then S01E01, S01E02... (default)
    - 'size_desc': Size: High to Low
    - 'size_asc': Size: Low to High
    - 'year_desc': Release Year: Newest first
    - 'recent': Recent uploads
    """
    if not files:
        return files
    def _get_size(f):
        if isinstance(f, dict):
            return f.get('file_size', 0)
        return getattr(f, 'file_size', 0)

    if sort_by == 'size_desc':
        return sorted(files, key=_get_size, reverse=True)
    elif sort_by == 'size_asc':
        return sorted(files, key=_get_size)
    elif sort_by == 'year_desc':
        return sorted(files, key=extract_year, reverse=True)
    elif sort_by == 'recent':
        return files
    else:
        return sort_files_season_first(files)


def is_file_locked(file_name: str) -> bool:
    """
    Checks if a file has a locked high resolution (4K / 2160p / 1440p / 1080p).
    """
    if not file_name:
        return False
    name_lower = str(file_name).lower()
    return any(q in name_lower for q in ['2160p', '4k', '1440p', '1080p', 'fhd', 'uhd'])


def format_file_button_label(file_name: str, file_size: int, is_vip: bool = False) -> str:
    """
    Formats the file button text:
    - Normal / VIP: 🔵 [size] filename
    - Free user with locked 1080p/4K resolution: 🟡 🔒 [{size}] {filename} [VIP]
    """
    cleaned = clean_file_name(file_name)
    size_str = get_size(file_size)
    if not is_vip and is_file_locked(file_name):
        return f"🟡 🔒 [{size_str}] {cleaned} [VIP]"
    return f"🔵 [{size_str}] {cleaned}"


def make_search_filter_buttons(req, key, active_filter=None):
    """
    Builds the standard RKMOVIESZIP Search Result interactive control buttons:
    🔴 Red: normal actions / sub-menus (Seasons, Episode, Language, Quality, Year, Sort)
    🟡 Yellow: VIP / Send All action
    active_filter: None, 'season', 'episode', 'lang', 'quality', 'year', 'sort'
    """
    send_all_btn = [
        InlineKeyboardButton("🟡 ! Sᴇɴᴅ Aʟʟ !", callback_data=f"sendfiles#{key}")
    ]

    seas_label = "🔴 ! Sᴇʟᴇᴄᴛ Aɢᴀɪɴ !" if active_filter == "season" else "🔴 Sᴇᴀꜱᴏɴꜱ"
    epi_label = "🔴 ! Sᴇʟᴇᴄᴛ Aɢᴀɪɴ !" if active_filter == "episode" else "🔴 Eᴘɪsᴏᴅᴇ"
    row1 = [
        InlineKeyboardButton(seas_label, callback_data=f"seas#{req}"),
        InlineKeyboardButton(epi_label, callback_data=f"epi#{req}")
    ]

    lang_label = "🔴 ! Sᴇʟᴇᴄᴛ Aɢᴀɪɴ !" if active_filter == "lang" else "🔴 Lᴀɴɢᴜᴀɢᴇ"
    qual_label = "🔴 ! Sᴇʟᴇᴄᴛ Aɢᴀɪɴ !" if active_filter == "quality" else "🔴 Qᴜᴀʟɪᴛʏꜱ"
    row2 = [
        InlineKeyboardButton(lang_label, callback_data=f"select_lang#{req}"),
        InlineKeyboardButton(qual_label, callback_data=f"quality#{req}")
    ]

    year_label = "🔴 ! Sᴇʟᴇᴄᴛ Aɢᴀɪɴ !" if active_filter == "year" else "🔴 Yᴇᴀʀ 📅"
    sort_label = "🔴 ! Sᴇʟᴇᴄᴛ Aɢᴀɪɴ !" if active_filter == "sort" else "🔴 Sᴏʀᴛ ⚡"
    row3 = [
        InlineKeyboardButton(year_label, callback_data=f"select_year#{req}"),
        InlineKeyboardButton(sort_label, callback_data=f"select_sort#{req}")
    ]

    return [send_all_btn, row1, row2, row3]


def get_time_until_midnight_ist():
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    target_time = time(23, 59, 59)
    target_datetime = tz.localize(datetime.combine(now.date(), target_time))
    if now > target_datetime:
        target_datetime += timedelta(days=1)
    time_diff = (target_datetime - now).total_seconds()
    hours = int(time_diff // 3600)
    minutes = int((time_diff % 3600) // 60)
    seconds = int(time_diff % 60)
    return hours, minutes, seconds


async def check_reset_time():
    tz = pytz.timezone('Asia/Kolkata')
    while True:
        now = datetime.now(tz)
        target_time = time(23, 59, 59)
        target_datetime = tz.localize(datetime.combine(now.date(), target_time))
        if now >= target_datetime:
            target_datetime += timedelta(days=1)
        time_diff = (target_datetime - now).total_seconds()
        hours = time_diff // 3600
        minutes = (time_diff % 3600) // 60
        seconds = time_diff % 60
        logging.info(f"Next reset in {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds.")
        await asyncio.sleep(time_diff)
        await db.reset_all_files_count()
        await db.reset_allsend_files()
        logging.info("Files count and send count reset successfully")
        await asyncio.sleep(5)  # Buffer to ensure next day has begun

async def get_seconds(time_string):
    def extract_value_and_unit(ts):
        value = ""
        unit = ""

        index = 0
        while index < len(ts) and ts[index].isdigit():
            value += ts[index]
            index += 1

        unit = ts[index:].lstrip()

        if value:
            value = int(value)

        return value, unit

    value, unit = extract_value_and_unit(time_string)

    if unit == 's':
        return value
    elif unit == 'min':
        return value * 60
    elif unit == 'hour':
        return value * 3600
    elif unit == 'day':
        return value * 86400
    elif unit == 'month':
        return value * 86400 * 30
    elif unit == 'year':
        return value * 86400 * 365
    else:
        return 0
        
async def is_req_subscribed(bot, query):
    if await db.find_join_req(query.from_user.id):
        return True
    try:
        user = await bot.get_chat_member(AUTH_CHANNEL, query.from_user.id)
    except UserNotParticipant:
        pass
    except Exception as e:
        print(e)
    else:
        if user.status != enums.ChatMemberStatus.BANNED:
            return True
    return False

async def is_subscribed(bot, user_id, channel_id):
    try:
        user = await bot.get_chat_member(channel_id, user_id)
    except UserNotParticipant:
        pass
    except Exception as e:
        pass
    else:
        if user.status != enums.ChatMemberStatus.BANNED:
            return True
    return False

async def get_poster(query, bulk=False, id=False, file=None):
    if not imdb:
        return None
    try:
        if not id:
            # https://t.me/GetTGLink/4183
            query = (query.strip()).lower()
            title = query
            year = re.findall(r'[1-2]\d{3}$', query, re.IGNORECASE)
            if year:
                year = list_to_str(year[:1])
                title = (query.replace(year, "")).strip()
            elif file is not None:
                year = re.findall(r'[1-2]\d{3}', file, re.IGNORECASE)
                if year:
                    year = list_to_str(year[:1]) 
            else:
                year = None
            movieid = imdb.search_movie(title.lower(), results=10)
            if not movieid:
                return None
            if year:
                filtered=list(filter(lambda k: str(k.get('year')) == str(year), movieid))
                if not filtered:
                    filtered = movieid
            else:
                filtered = movieid
            movieid=list(filter(lambda k: k.get('kind') in ['movie', 'tv series'], filtered))
            if not movieid:
                movieid = filtered
            if bulk:
                return movieid
            movieid = movieid[0].movieID
        else:
            movieid = query
        movie = imdb.get_movie(movieid)
        if not movie:
            return None
        if movie.get("original air date"):
            date = movie["original air date"]
        elif movie.get("year"):
            date = movie.get("year")
        else:
            date = "N/A"
        plot = ""
        if not LONG_IMDB_DESCRIPTION:
            plot = movie.get('plot')
            if plot and len(plot) > 0:
                plot = plot[0]
        else:
            plot = movie.get('plot outline')
        if plot and len(plot) > 800:
            plot = plot[0:800] + "..."

        return {
            'title': movie.get('title'),
            'votes': movie.get('votes'),
            "aka": list_to_str(movie.get("akas")),
            "seasons": movie.get("number of seasons"),
            "box_office": movie.get('box office'),
            'localized_title': movie.get('localized title'),
            'kind': movie.get("kind"),
            "imdb_id": f"tt{movie.get('imdbID')}",
            "cast": list_to_str(movie.get("cast")),
            "runtime": list_to_str(movie.get("runtimes")),
            "countries": list_to_str(movie.get("countries")),
            "certificates": list_to_str(movie.get("certificates")),
            "languages": list_to_str(movie.get("languages")),
            "director": list_to_str(movie.get("director")),
            "writer":list_to_str(movie.get("writer")),
            "producer":list_to_str(movie.get("producer")),
            "composer":list_to_str(movie.get("composer")) ,
            "cinematographer":list_to_str(movie.get("cinematographer")),
            "music_team": list_to_str(movie.get("music department")),
            "distributors": list_to_str(movie.get("distributors")),
            'release_date': date,
            'year': movie.get('year'),
            'genres': list_to_str(movie.get("genres")),
            'poster': movie.get('full-size cover url'),
            'plot': plot,
            'rating': str(movie.get("rating")),
            'url':f'https://www.imdb.com/title/tt{movieid}'
        }
    except Exception as e:
        logger.warning(f"Error occurred while fetching poster/IMDb details: {e}")
        return None
# https://github.com/odysseusmax/animated-lamp/blob/2ef4730eb2b5f0596ed6d03e7b05243d93e3415b/bot/utils/broadcast.py#L37

async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - Removed from Database, since deleted account.")
        return False, "Deleted"
    except UserIsBlocked:
        logging.info(f"{user_id} - Blocked the bot.")
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - PeerIdInvalid")
        return False, "Error"
    except Exception as e:
        return False, "Error"

async def get_settings(group_id):
    settings = temp.SETTINGS.get(group_id)
    if not settings:
        settings = await db.get_settings(group_id)
        temp.SETTINGS[group_id] = settings
    return settings
    
async def save_group_settings(group_id, key, value):
    current = await get_settings(group_id)
    current[key] = value
    temp.SETTINGS[group_id] = current
    await db.update_settings(group_id, current)

def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])
    
def list_to_str(k): 
    if not k:
        return "N/A"
    elif len(k) == 1:
        return str(k[0])
    else:
        return ' '.join(f'{elem}, ' for elem in k)
        
def get_file_id(msg: Message):
    if msg.media:
        for message_type in (
            "photo",
            "animation",
            "audio",
            "document",
            "video",
            "video_note",
            "voice",
            "sticker"
        ):
            obj = getattr(msg, message_type)
            if obj:
                setattr(obj, "message_type", message_type)
                return obj

def extract_user(message: Message) -> Union[int, str]:
    """extracts the user from a message"""
    # https://github.com/SpEcHiDe/PyroGramBot/blob/f30e2cca12002121bad1982f68cd0ff9814ce027/pyrobot/helper_functions/extract_user.py#L7
    user_id = None
    user_first_name = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_first_name = message.reply_to_message.from_user.first_name

    elif len(message.command) > 1:
        if (
            len(message.entities) > 1 and
            message.entities[1].type == enums.MessageEntityType.TEXT_MENTION
        ):
           
            required_entity = message.entities[1]
            user_id = required_entity.user.id
            user_first_name = required_entity.user.first_name
        else:
            user_id = message.command[1]
            # don't want to make a request -_-
            user_first_name = user_id
        try:
            user_id = int(user_id)
        except ValueError:
            pass
    else:
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name
    return (user_id, user_first_name)
         

async def stream_site(link, grp_id):
    try:
        settings = await get_settings(grp_id) if await get_settings(grp_id) else {}
        api_key, site_key = ('streamapi', 'streamsite')
        default_api, default_site = STREAM_API, STREAM_SITE
        
        api = settings.get(api_key, default_api)
        site = settings.get(site_key, default_site)

        shortzy = Shortzy(api, site)

        try:
            link = await shortzy.convert(link)
        except Exception:
            link = await shortzy.get_quick_link(link)
        return link
    except Exception as e:
        logger.error(e)

async def get_shortlink(link, grp_id, is_second_shortener=False, is_third_shortener=False):
    try:
        settings = await get_settings(grp_id) if await get_settings(grp_id) else {}
        if is_third_shortener:
            api_key, site_key = ('verify_api3', 'verify_3')
            default_api, default_site = VERIFY_API3, VERIFY_URL3
        elif is_second_shortener:
            api_key, site_key = ('verify_api2', 'verify_2')
            default_api, default_site = VERIFY_API2, VERIFY_URL2
        else:
            api_key, site_key = ('verify_api', 'verify')
            default_api, default_site = VERIFY_API, VERIFY_URL

        api = settings.get(api_key, default_api)
        site = settings.get(site_key, default_site)
        shortzy = Shortzy(api, site)
        try:
            link = await shortzy.convert(link)
        except Exception:
            link = await shortzy.get_quick_link(link)
        return link
    except Exception as e:
        logger.error(f"Error in get_shortlink: {e}")
        return link

async def get_users():
    count  = await user_col.count_documents({})
    cursor = user_col.find({})
    list   = await cursor.to_list(length=int(count))
    return count, list

async def get_text(settings, remaining_seconds, files, query, total_results, search):
    try:
        files = sort_files_season_first(files)
        if settings["imdb"]:
            IMDB_CAP = temp.IMDB_CAP.get(query.from_user.id)
            CAPTION = f"☠️ ᴛɪᴛʟᴇ : <code>{search}</code>\n📂 ᴛᴏᴛᴀʟ ꜰɪʟᴇꜱ : <code>{total_results}</code>\n📝 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : {query.from_user.first_name}\n⏰ ʀᴇsᴜʟᴛ ɪɴ : <code>{remaining_seconds} Sᴇᴄᴏɴᴅs</code>\n\n</b>"
            if IMDB_CAP:
                cap = IMDB_CAP
                for file in files: #shortlink = false, imdb = true
                    cap += f"\n\n<b><a href='https://telegram.me/{temp.U_NAME}?start=files_{query.message.chat.id}_{file.file_id}'>🔵 {get_size(file.file_size)} ▷ {clean_file_name(file.file_name)}</a></b>"
            else:
                imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
                if imdb:
                    TEMPLATE = script.IMDB_TEMPLATE_TXT
                    cap = TEMPLATE.format(
                        qurey=search,
                        title=imdb['title'],
                        votes=imdb['votes'],
                        aka=imdb["aka"],
                        seasons=imdb["seasons"],
                        box_office=imdb['box_office'],
                        localized_title=imdb['localized_title'],
                        kind=imdb['kind'],
                        imdb_id=imdb["imdb_id"],
                        cast=imdb["cast"],
                        runtime=imdb["runtime"],
                        countries=imdb["countries"],
                        certificates=imdb["certificates"],
                        languages=imdb["languages"],
                        director=imdb["director"],
                        writer=imdb["writer"],
                        producer=imdb["producer"],
                        composer=imdb["composer"],
                        cinematographer=imdb["cinematographer"],
                        music_team=imdb["music_team"],
                        distributors=imdb["distributors"],
                        release_date=imdb['release_date'],
                        year=imdb['year'],
                        genres=imdb['genres'],
                        poster=imdb['poster'],
                        plot=imdb['plot'],
                        rating=imdb['rating'],
                        url=imdb['url'],
                        **locals()
                    )
                    for file in files:
                        badge = "🟡 🔒 " if is_file_locked(file.file_name) else "🔵 "
                        vip_tag = " [VIP]" if is_file_locked(file.file_name) else ""
                        cap += f"\n\n<b><a href='https://telegram.me/{temp.U_NAME}?start=files_{query.message.chat.id}_{file.file_id}'>{badge}{get_size(file.file_size)} ▷ {clean_file_name(file.file_name)}{vip_tag}</a></b>"
                else:
                    cap = f"{CAPTION}" #imdb = false
                    cap+="<b>📚 <u>Your Requested Files</u> 👇\n\n</b>"
                    for file in files:
                        badge = "🟡 🔒 " if is_file_locked(file.file_name) else "🔵 "
                        vip_tag = " [VIP]" if is_file_locked(file.file_name) else ""
                        cap += f"<b><a href='https://telegram.me/{temp.U_NAME}?start=files_{query.message.chat.id}_{file.file_id}'>{badge}{get_size(file.file_size)} ▷ {clean_file_name(file.file_name)}{vip_tag}\n\n</a></b>"
    
        else:
            #imdb = false
            cap = f"☠️ ᴛɪᴛʟᴇ : <code>{search}</code>\n📂 ᴛᴏᴛᴀʟ ꜰɪʟᴇꜱ : <code>{total_results}</code>\n📝 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : {query.from_user.first_name}\n⏰ ʀᴇsᴜʟᴛ ɪɴ : <code>{remaining_seconds}\n\n</b>"
            cap+="<b>📚 <u>Your Requested Files</u> 👇\n\n</b>"
            for file in files:
                badge = "🟡 🔒 " if is_file_locked(file.file_name) else "🔵 "
                vip_tag = " [VIP]" if is_file_locked(file.file_name) else ""
                cap += f"<b><a href='https://telegram.me/{temp.U_NAME}?start=files_{query.message.chat.id}_{file.file_id}'>{badge}{get_size(file.file_size)} ▷ {clean_file_name(file.file_name)}{vip_tag}\n\n</a></b>"
        return cap
    except Exception as e:
        await query.answer(f"{e}", show_alert=True)
        return cap
