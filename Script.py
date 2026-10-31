import random


_NOTIFICATION_LAST_USED = {}


NOTIFICATION_MESSAGES = {
    "not_your_file": [
        "{}, ye movie request tumhari nahi hai 😏",
        "Nice try 😉 ye wali file kisi aur ki request hai.",
        "Arre naughty 😈 dusre ki file pe nazar?",
        "Hmm 😌 ye request tumhare naam ki nahi hai.",
        "Oops cutie ❤️ is file ke liye apni request use karo.",
        "Pakde gaye 😏 ye movie request tumhari nahi hai.",
    ],
    "file_not_found": [
        "Aww 😏 ye file toh sharma ke gayab ho gayi.",
        "Uff 😉 ye wali file mili hi nahi, cutie.",
        "Hmm 😌 file kahaan chhup gayi?",
        "Oops 😈 ye movie hide-and-seek khel rahi hai.",
        "Sorry sweetheart ❤️ ye file nahi mili.",
        "Nice try 😏 is baar file haath nahi aayi.",
    ],
    "premium_required": [
        "Ye wali movie VIP hai jaan 😏 Premium chahiye 🔐",
        "Hmm 😉 ads-free magic sirf Premium ke liye hai.",
        "Nice try cutie 😈 VIP access unlock karo.",
        "Ye file thodi special treatment maang rahi hai 😌🔐",
        "Premium ke bina ye secret door nahi khulega 😉",
        "Jaan, is feature ko Premium wali attention chahiye 😏",
    ],
    "error": [
        "Uff 😮‍💨 thoda technical nakhra aa gaya:\n{}",
        "Aww 😅 system ne thodi sharaarat kar di:\n{}",
        "Oops cutie 😈 ek temporary glitch mil gaya:\n{}",
        "Hmm 😌 kuch technical gadbad hui:\n{}",
        "Arre baby 😉 bot ko chhota sa error mila:\n{}",
    ],
    "select_language": [
        "Cutie 😉 neeche se koi language choose karo.",
        "Hmm 😏 movie ki language pick karo, sweetheart.",
        "Aww 😌 ek language select kar do na.",
        "Nice try 😈 pehle apni language choose karo.",
        "Baby ❤️ language button dabao, phir movie milegi.",
        "Uff 😉 bas language select karni hai, easy peasy.",
    ],
    "select_quality": [
        "Jaan 😏 neeche se koi quality choose karo.",
        "Hmm 😉 apni favourite quality pick karo, cutie.",
        "Aww 😌 movie ki quality select kar do.",
        "Nice try 😈 pehle quality choose karo.",
        "Baby ❤️ quality button tumhara wait kar raha hai.",
        "Uff 😉 HD ya jo pasand ho, select karo.",
    ],
    "select_season": [
        "Cutie 😏 pehle season choose karo.",
        "Hmm 😉 kaunsa season chahiye, sweetheart?",
        "Aww 😌 season select karo, phir next scene.",
        "Nice try 😈 neeche se season pick karo.",
        "Baby ❤️ apna season choose kar lo.",
        "Uff 😉 season button ko ignore mat karo.",
    ],
    "select_episode": [
        "Jaan 😏 pehle episode choose karo.",
        "Hmm 😉 kaunsa episode dekhna hai, cutie?",
        "Aww 😌 episode select karo, movie mood on.",
        "Nice try 😈 neeche se episode pick karo.",
        "Baby ❤️ apna episode choose kar lo.",
        "Uff 😉 episode button tumhara wait kar raha hai.",
    ],
    "select_year": [
        "Cutie 😏 release year choose karo na.",
        "Hmm 😉 kaunse saal ki movie chahiye, sweetheart?",
        "Aww 😌 year select karo, phir dekhte hain magic.",
        "Nice try 😈 neeche se year pick karo.",
        "Baby ❤️ apna favourite release year select karo.",
        "Uff 😉 year button tumhara wait kar raha hai.",
    ],
    "select_sort": [
        "Cutie 😏 sort order select karo.",
        "Hmm 😉 files kis order mein arrange karun, sweetheart?",
        "Aww 😌 sort option choose karo, baby.",
        "Nice try 😈 size ya season order pick karo.",
        "Baby ❤️ apni pasand ka sort select kar lo.",
        "Uff 😉 order sort karke sab easy kar deti hoon.",
    ],
    "sort_applied": [
        "Sort ho gaya cutie 😏 ab dekho list!",
        "Done baby 😉 files arrange kar di hain.",
        "Aww 😌 tumhari pasand se order set ho gaya.",
        "Nice 😈 nayi sorting ke saath files ready hain.",
    ],
    "send_all_vip": [
        "Ye VIP hai cutie 😏 Saari files ek saath chahiye toh VIP le lo!",
        "Aww baby 😏 Send All sirf VIP members ke liye reserved hai.",
        "Nice try darling 😈 Ek-ek karke download kar lo ya fir VIP ban jao!",
        "Ye feature VIP hai jaan 😏 Sab ek click me lene ke liye VIP unlock karo.",
        "Bas baby 😏 Send All VIP privilege hai, VIP plans check karo na!",
    ],
    "shortener_bypass_vip": [
        "VIP privilege activated cutie 😏 Shortener direct bypass!",
        "Aww baby 😉 VIP ho toh no ads, no shortener direct file le lo!",
        "VIP power darling 😈 Shortener bypass ho gaya, enjoy!",
        "Sweetheart 😏 VIP ho isliye seedha direct link!",
    ],
    "resolution_locked": [
        "Ye HD/4K quality VIP hai cutie 😏 Crystal clear maza VIP me hai!",
        "Aww baby 😏 1080p aur 4K sirf VIP members ke liye reserved hai.",
        "Nice taste darling 😈 Lekin ye Ultra HD quality VIP exclusive hai!",
        "Cutie 😏 4K prints chahiye toh VIP unlock karo na!",
        "Ye resolution VIP locked hai baby 😏 720p dekh lo ya VIP ban jao!",
    ],
    "unlock_bot": [
        "Aww 😏 pehle bot unlock karo, phir movie milegi.",
        "Hmm 😉 bot ko unlock kar do, cutie.",
        "Uff 😮‍💨 pehle unlock, phir full movie vibes.",
        "Nice try 😈 bot unlock karo sweetheart.",
        "Baby ❤️ unlock karte hi movie journey start.",
        "Cutie 😌 ek unlock tap aur kaam done.",
    ],
    "access_denied": [
        "Oops 😏 ye action tumhare access mein nahi hai.",
        "Hmm 😉 permission ke bina ye door nahi khulega.",
        "Aww 😌 is option ke liye access chahiye.",
        "Nice try 😈 tumhe abhi permission nahi hai.",
        "Cutie ❤️ ye setting authorized users ke liye hai.",
        "Uff 😉 access denied, sweetheart.",
    ],
    "admin_only": [
        "Oops 😏 ye corner sirf bot admins ke liye hai.",
        "Hmm 😉 admin access chahiye, cutie.",
        "Nice try 😈 ye button VIP admins ke liye reserved hai.",
        "Aww 😌 sirf bot admin ye kaam kar sakta hai.",
        "Uff 😉 admin zone hai, sweetheart.",
        "Baby ❤️ ye option abhi admins only hai.",
    ],
    "searching": [
        "Aww 😏 tumhari movie dhoond rahi hoon... 🔍",
        "Hmm 😉 database mein tumhari movie search ho rahi hai.",
        "Uff 😮‍💨 movie hunt on hai, cutie... 🔍",
        "Nice try 😈 files ko tumhare liye scan kar rahi hoon.",
        "Baby 😌 thoda wait, movie ko pakad rahi hoon.",
        "Cutie ❤️ search chal rahi hai... ek sec.",
    ],
    "generic": [
        "Hmm 😏 button toh daba diya, cutie.",
        "Aww 😉 nice try, sweetheart.",
        "Uff 😮‍💨 thoda movie magic aur.",
        "Hehe 😈 kuch dekhne layak dhoond rahe ho?",
        "Okay cutie 😌 next move karo.",
        "Baby ❤️ main yahin hoon, try karo.",
    ],
    "referral_points": [
        "Aww 😏 tumhare paas {} referral points hain.",
        "Hmm 😉 sweetheart, balance hai {} referral points.",
        "Nice 😌 tumne {} referral points collect kiye hain.",
        "Uff 😈 total {} referral points, cutie.",
        "Baby ❤️ tumhara referral score {} points hai.",
        "Cutie 😉 abhi tumhare {} referral points hain.",
    ],
    "checking_database": [
        "Aww 😏 database mein check kar rahi hoon...",
        "Hmm 😉 files database mein dekh rahi hoon.",
        "Uff 😮‍💨 database scan ho raha hai, cutie...",
        "Nice try 😈 records check kar rahi hoon...",
        "Baby 😌 database ko ek quick look de rahi hoon.",
        "Cutie ❤️ files verify kar rahi hoon...",
    ],
    "reset_success": [
        "Aww 😏 settings reset ho gayi, cutie.",
        "Done 😉 group settings fresh kar di gayi hain.",
        "Hmm 😌 reset complete, sweetheart.",
        "Nice 😈 settings ka makeover ho gaya.",
        "Uff 😉 reset successful, baby.",
        "Cutie ❤️ settings neatly reset ho gayi.",
    ],
    "index_cancel": [
        "Aww 😌 indexing cancel kar di gayi.",
        "Hmm 😉 indexing ruk gayi, cutie.",
        "Uff 😮‍💨 indexing ko pause kar diya.",
        "Okay 😏 indexing cancel ho gayi.",
        "Nice try 😈 indexing stop kar di.",
        "Baby ❤️ indexing cancel ho gayi.",
    ],
    "index_wait": [
        "Uff 😮‍💨 pehle wala process chal raha hai, thoda wait.",
        "Hmm 😉 ek indexing already busy hai, cutie.",
        "Aww 😌 current process finish hone do.",
        "Nice try 😏 pehle wali indexing ko complete hone do.",
        "Baby ❤️ thoda wait, process already running hai.",
        "Uff 😉 queue mein ho, sweetheart.",
    ],
    "index_processing": [
        "Aww 😏 indexing start ho rahi hai... ⏳",
        "Hmm 😉 files process kar rahi hoon, cutie.",
        "Uff 😮‍💨 indexing in progress...",
        "Nice try 😈 database mein files set kar rahi hoon.",
        "Baby 😌 processing start ho gayi.",
        "Cutie ❤️ indexing ka kaam shuru hai.",
    ],
    "group_not_found": [
        "Aww 😕 ye group toh mil hi nahi raha.",
        "Hmm 😉 group kahaan gaya, cutie?",
        "Uff 😮‍💨 requested group nahi mila.",
        "Oops 😈 ye group database mein nahi mila.",
        "Sorry sweetheart ❤️ group not found.",
        "Nice try 😏 is group ka record nahi mila.",
    ],
    "group_verified": [
        "Aww 😏 group verify ho gaya successfully ✅",
        "Nice 😉 group approved aur verified hai.",
        "Hmm 😌 verification complete, sweetheart. ✅",
        "Uff 😈 group ne VIP entry le li. Verified ✅",
        "Baby ❤️ group successfully verified.",
        "Cutie 😉 verification done, all set. ✅",
    ],
    "group_rejected": [
        "Uff 😮‍💨 group verification reject ho gayi ❌",
        "Hmm 😕 is baar group approve nahi hua.",
        "Aww 😌 verification request reject ho gayi.",
        "Nice try 😈 group ko abhi approval nahi mila.",
        "Sorry sweetheart ❤️ group rejected hai.",
        "Oops 😉 verification pass nahi hui.",
    ],
    "no_search_result": [
        "<i>Aww 😏 {} ke liye kuch nahi mila… spelling check karke phir try karo.</i>",
        "<i>Hmm 😉 {} search mein nahi mila. Thoda sa movie-name tweak karo.</i>",
        "<i>Uff 😮‍💨 {} ne aaj hide-and-seek jeet li. Ek baar phir try karo.</i>",
        "<i>Oops 😈 {} ka result nahi mila. Cutie, naam dobara check karo.</i>",
        "<i>Sorry sweetheart ❤️ {} ka matching result nahi mila. Try again.</i>",
        "<i>Nice try 😌 {} ka match nahi mila. Sahi title ke saath phir search karo.</i>",
    ],
    "link_expired": [
        "Aww 😮‍💨 ye link expire ho gaya, cutie. Dobara try karo.",
        "Uff 😉 link ka time khatam ho gaya, sweetheart.",
        "Hmm 😌 ye link ab active nahi hai. Fresh try karo.",
        "Oops 😈 link expire ho chuka hai. Ek baar phir tap karo.",
        "Sorry baby ❤️ ye link old ho gaya. Naya try karo.",
        "Nice try 😏 expired link ko fresh request chahiye.",
    ],
    "force_subscribe": [
        "Aww 😏 pehle channel join karo, phir movie tumhari.",
        "Hmm 😉 channel join kar lo, cutie, phir file unlock hogi.",
        "Uff 😮‍💨 pehle channel wali entry complete karo.",
        "Nice try 😈 channel join ke bina movie nahi milegi.",
        "Baby ❤️ pehle join karo, phir movie enjoy karo.",
        "Sweetheart 😌 channel join karo aur phir dobara try karo.",
    ],
    "file_limit": [
        "Uff 😮‍💨 daily file limit reach ho gayi, jaan. Premium se unlimited karo.",
        "Aww 😏 aaj ki file limit full hai, cutie. Premium unlock karo.",
        "Hmm 😉 limit ne aaj brake laga di. Premium se continue karo.",
        "Nice try 😈 daily limit complete. VIP/Premium se next files unlock karo.",
        "Baby ❤️ file limit khatam ho gayi. Premium mein full access milega.",
        "Oops 😌 quota full ho gaya, sweetheart. Premium se smooth ride rakho.",
    ],
    "button_limit": [
        "Uff 😮‍💨 Send All limit reach ho gayi, cutie. Premium chahiye.",
        "Aww 😏 button limit full hai. Premium se unlimited use karo.",
        "Hmm 😉 aaj ka Send All quota complete ho gaya.",
        "Nice try 😈 limit hit ho gayi. VIP access se continue karo.",
        "Baby ❤️ button limit khatam hai. Premium unlock kar lo.",
        "Oops 😌 quota full, sweetheart. Premium se phir full speed.",
    ],
    "already_done": [
        "Aww 😏 ye kaam already done hai.",
        "Hmm 😉 sweetheart, ye group pehle hi verified hai. ✅",
        "Nice 😌 ye step tum already complete kar chuke ho.",
        "Uff 😈 double-check ki zaroorat nahi, already done.",
        "Baby ❤️ ye kaam pehle hi ho chuka hai.",
        "Cutie 😉 already sorted, kuch aur try karo.",
    ],
}


def get_random_message(category, *args):
    messages = NOTIFICATION_MESSAGES[category]
    if len(messages) == 1:
        index = 0
    else:
        index = random.randrange(len(messages))
        while _NOTIFICATION_LAST_USED.get(category) == index:
            index = random.randrange(len(messages))
    _NOTIFICATION_LAST_USED[category] = index
    message = messages[index].format(*args)
    if category in {"not_your_file", "file_not_found", "premium_required", "send_all_vip", "shortener_bypass_vip", "resolution_locked", "error", "select_language", "select_quality", "select_season", "select_episode", "select_year", "select_sort", "sort_applied", "unlock_bot", "access_denied", "admin_only", "searching", "generic", "referral_points", "checking_database", "reset_success", "index_cancel", "index_wait", "index_processing", "group_not_found", "group_verified", "group_rejected", "already_done", "link_expired"} and len(message) > 200:
        message = message[:197] + "..."
    return message


class script(object):
    START_TXT = """<b><i>ʜᴇʏ 😎</i></b> {},
<b><blockquote>Iᴍ Tʜᴇ Mᴏsᴛ Aᴅᴠᴀɴᴄᴇ Aɪ Pᴏᴡᴇʀᴅ Bᴏᴛ.🥰
Jᴜꜱᴛ Sᴇɴᴅ Mᴇ Aɴʏ Mᴏᴠɪᴇꜱ & Sᴇʀɪᴇꜱ Nᴀᴍᴇ Aɴᴅ Sᴇᴇ Mʏ Pᴏᴡᴇʀ.</b></blockquote>

<b><spoiler>🔋 ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ - <a href=https://t.me/Looterekrish>Lₒₒ𝚝ₑᵣₑ™</b></spoiler></a>"""
    
    HELP_TXT = """<b>ʜᴇʏ {},
ᴡᴇ ʜᴀᴠᴇ ᴅᴇᴠɪᴅᴇᴅ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅꜱ ꜰᴏʀ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀꜱ ᴀɴᴅ ʙᴏᴛ ᴜꜱᴇʀꜱ.</b>"""

    
    BLACKLIST = ['tamilblaster', 'filmyzilla', 'streamershub', 'xyz', 'cine', 'www', 'http', 'https',
                'cloudsmoviesstore', 'moviez2you', 'bkp', 'cinema', 'filmy', 'flix', 'cutemoviez',
                '4u', 'hub', 'movies', 'otthd', 'telegram', 'hoichoihok', '@', ']', '[', 'missqueenbotx',
                'filmy', 'films', 'cinema', 'join', 'club', 'apd', 'F-Press', 'GDTOT', 'mkv', 'NETFLIX_OFFICIAL',
                'backup', 'primeroom', 'theprofffesorr', 'premium', 'vip', '4wap', 'toonworld4all', 'mlwbd',
                'Telegram@alpacinodump', 'bollywood', "AllNewEnglishMovie", "7MovieRulz", "1TamilMV",
                'Bazar', '_Corner20', 'CornersOfficial', 'support', 'iMediaShare', 'Uᴘʟᴏᴀᴅᴇᴅ', 'Bʏ', 'PFM', 'alpacinodump', 
                "Us", "boxoffice", "Links", "Linkz", "Villa", "Original", "bob", "Files1", "MW", "LinkZ", "}", "{" 
                ]
    
    
    REFFER_TXT = """
<b>ʀᴇғᴇʀʀᴇ ʏᴏᴜʀ ғʀɪᴇɴᴅs ᴀɴᴅ ғᴀᴍɪʟʏ, ᴀɴᴅ ᴄᴏʟʟᴇᴄᴛ 50 ᴘᴏɪɴᴛ

Note: = ᴘᴇʀ ʀᴇғғᴇʀ 10 ᴘᴏɪɴᴛ

ʏᴏᴜʀ ʀᴇғᴇʀᴀʟ ʟɪɴᴋ - https://telegram.me/{}?start=reff_{}

ɪғ ʏᴏᴜ ᴄᴏʟʟᴇᴄᴛ 50 ᴘᴏɪɴᴛs, ʏᴏᴜ ᴡɪʟʟ ʙᴇ ɢɪᴠᴇɴ 1 ᴍᴏɴᴛʜ ᴘʀᴇᴍɪᴜᴍ.
============================
 <u>💫ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs💫</u> :

○ sᴇᴀʀᴄʜ ᴍᴏᴠɪᴇ ɪɴ ᴛʜᴇ ʙᴏᴛ
○ ɴᴏ ғɪʟᴇ ʟɪᴍɪᴛs
○ ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ғɪʟᴇs
○ ɴᴏ ʟɪᴍɪᴛs ғᴏʀ sᴇɴᴅ ᴀʟʟ ʙᴜᴛᴛᴏɴ
○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋꜱ
○ ɴᴏ ɴᴇᴇᴅ ᴠᴇʀɪғʏ
○ ᴅɪʀᴇᴄᴛ ғɪʟᴇs   
○ ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ 
○ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs & sᴇʀɪᴇs        
____________________________
ʙᴜʏ ᴘᴀɪᴅ ᴘʟᴀɴ ʙʏ - /plans</b>"""

    FSUB_TXT = """<i><b>🙁 ғɪʀꜱᴛ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛʜᴇɴ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴍᴏᴠɪᴇ, ᴏᴛʜᴇʀᴡɪꜱᴇ ʏᴏᴜ ᴡɪʟʟ ɴᴏᴛ ɢᴇᴛ ɪᴛ.

ᴄʟɪᴄᴋ ᴊᴏɪɴ ɴᴏᴡ ʙᴜᴛᴛᴏɴ 👇</b></i>"""

    VERIFICATION_TEXT = """<b>ʜᴇʏ {}, cutie 😏

<u>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ ᴛᴏᴅᴀʏ, ᴘʟᴇᴀꜱᴇ ᴄʟɪᴄᴋ ᴏɴ ᴠᴇʀɪғʏ & ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇꜱꜱ ғᴏʀ ᴛɪʟʟ ɴᴇxᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ</u> ⚡️

#ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ:- 1/3

<i>Baby, ads aur shorteners se bachna ho toh VIP le lo aur direct files paao! 🍿👑</i>

💶 ꜱᴇɴᴅ /plans ᴛᴏ ʙᴜʏ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ</b>"""

    SECOND_VERIFICATION_TEXT = """<b>ʜᴇʏ {}, jaan 😉

<u>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪꜰɪᴇᴅ ‼️
ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪꜰɪᴇᴅ, ᴛᴀᴘ ᴏɴ ᴛʜᴇ ᴠᴇʀɪꜰʏ ʟɪɴᴋ ᴀɴᴅ ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ꜰᴏʀ ᴛɪʟʟ ɴᴇxᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ🔋</u>

#ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ:- 2/3

<i>Shorteners se aazadi chahiye toh VIP membership try karo cutie! 👑</i>

💶 ꜱᴇɴᴅ /plans ᴛᴏ ʙᴜʏ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ</b>"""
    
    THIRDT_VERIFICATION_TEXT = """<b>ʜᴇʏ {}, sweetheart 😈
    
📌 <u>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪꜰɪᴇᴅ ᴛᴏᴅᴀʏ, ᴛᴀᴘ ᴏɴ ᴛʜᴇ ᴠᴇʀɪꜰʏ ʟɪɴᴋ & ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ꜰᴏʀ ɴᴇxᴛ ꜰᴜʟʟ ᴅᴀʏ.</u>

#ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ:- 3/3

<i>Direct, fast & ad-free files sirf VIP members ke liye hain baby! 🍿</i></b>"""

    
    
    VERIFY_COMPLETE_TEXT = """<b>ʜᴇʏ {},

ʏᴏᴜ ʜᴀᴠᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴛʜᴇ 1st ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ✅...

ɴᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ғᴏʀ ɴᴇxᴛ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ...

ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴅɪʀᴇᴄᴛ ғɪʟᴇꜱ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴꜱ ᴛʜᴇɴ ʙᴜʏ ʙᴏᴛ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ 

💶 ꜱᴇɴᴅ /plans ᴛᴏ ʙᴜʏ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ</b>"""


    SECOND_COMPLETE_TEXT = """<b>ʜᴇʏ {},

ʏᴏᴜ ʜᴀᴠᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ sᴇᴄᴏɴᴅ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ✅...

ɴᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ғᴏʀ ɴᴇxᴛ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ

ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴅɪʀᴇᴄᴛ ғɪʟᴇꜱ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴꜱ ᴛʜᴇɴ ʙᴜʏ ʙᴏᴛ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ 

💶 ꜱᴇɴᴅ /plans ᴛᴏ ʙᴜʏ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ</b>"""

    THIRDT_COMPLETE_TEXT= """<b> ʜᴇʏ {}, 
    
ʏᴏᴜ ʜᴀᴠᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴛʜᴇ 3rd ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ✅

ɴᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ꜰᴏʀ ɴᴇxᴛ ꜰᴜʟʟ ᴅᴀʏ </b>"""


    VERIFIED_LOG_TEXT = """<b><u>☄ ᴜsᴇʀ ᴠᴇʀɪꜰɪᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ ☄</u>

⚡️ ɴᴀᴍᴇ:- {} [ <code>{}</code> ] 
📆 ᴅᴀᴛᴇ:- <code>{} </code></b>

#verified_{}_completed"""
    
    FILE_LIMIT = """
📁 ʏᴏᴜʀ ғɪʟᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ

ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ғɪʟᴇs ᴛʜᴇɴ ᴛᴀᴋᴇ ᴘʀᴇᴍɪᴜᴍ

💲sᴇᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs /plans

ʀᴇsᴇᴛ ᴛɪᴍᴇ ⌚ = 11.59 PM.
"""
    BUTTON_LIMIT = """
sᴇɴᴅ ᴀʟʟ ʙᴜᴛᴛᴏɴ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ

ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ʙᴜᴛᴛᴏɴ ᴜsᴇ ᴛʜᴇɴ ᴛᴀᴋᴇ ᴘʀᴇᴍɪᴜᴍ

💲sᴇᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs /plans

ʀᴇsᴇᴛ ᴛɪᴍᴇ ⌚ = 11.59 PM.
"""

    ABOUT_TXT = """<b>
‣ ᴍʏ ɴᴀᴍᴇ : <a href=https://t.me/{}>{}</a>
‣ ᴄʀᴇᴀᴛᴏʀ : <a href=https://t.me/Looterekrish>Lₒₒ𝚝ₑᵣₑ™</a>
‣ ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ
‣ ʟᴀɴɢᴜᴀɢᴇ : ᴘʏᴛʜᴏɴ
‣ ᴅᴀᴛᴀ ʙᴀsᴇ : ᴍᴏɴɢᴏ ᴅʙ
‣ ʜᴏsᴛᴇᴅ ᴏɴ  : ʜᴇʀᴏᴋᴜ
‣ ʙᴜɪʟᴅ sᴛᴀᴛᴜs : ᴠ4.2 [sᴛᴀʙʟᴇ]</b>"""

    FEATURES = """💥 ғᴇᴀᴛᴜʀᴇs ᴀʟʟ ʟɪsᴛ 💥
    
‣ /telegraph - Sᴇɴᴅ Mᴇ Pʜᴏᴛᴏ Oʀ Vɪᴅᴇᴏ Uɴᴅᴇʀ(5ᴍʙ) Aɴᴅ Rᴇᴘʟʏ Wɪᴛʜ Cᴏᴍᴍᴀᴍɴᴅ

‣ /font - ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴍᴏᴅᴇ ᴛᴏ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ꜰᴏɴᴛs sᴛʏʟᴇ

ᴇxᴛʀᴀ ғᴇᴀᴛᴜʀᴇ ᴄᴏᴍɪɴɢ"""

    
    STATUS_TXT = """<b>★ Tᴏᴛᴀʟ Fɪʟᴇs: <code>{}</code>
★ Tᴏᴛᴀʟ Usᴇʀs: <code>{}</code>
★ Tᴏᴛᴀʟ Cʜᴀᴛs: <code>{}</code>
★ Usᴇᴅ Sᴛᴏʀᴀɢᴇ: <code>{}</code>
★ Fʀᴇᴇ Sᴛᴏʀᴀɢᴇ: <code>{}</code></b>"""

    LOG_TEXT_G = """#NewGroup
BOT {}
Gʀᴏᴜᴘ = {}(<code>{}</code>)
Tᴏᴛᴀʟ Mᴇᴍʙᴇʀs = <code>{}</code>
Aᴅᴅᴇᴅ Bʏ - {}"""

    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Nᴀᴍᴇ - {}
Bᴏᴛ {}"""

    ALRT_TXT = """{},
ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ʏᴏᴜʀ ᴍᴏᴠɪᴇ ʀᴇQᴜᴇꜱᴛ,
ʀᴇQᴜᴇꜱᴛ ʏᴏᴜʀ'ꜱ..."""

    CUDNT_FND = """<i>ɪ ᴄᴏᴜʟᴅɴ'ᴛ ꜰɪɴᴅ ᴀɴʏᴛʜɪɴɢ ʀᴇʟᴀᴛᴇᴅ ᴛᴏ {}
ᴅɪᴅ ʏᴏᴜ ᴍᴇᴀɴ ᴀɴʏ ᴏɴᴇ ᴏꜰ ᴛʜᴇꜱᴇ?</i>"""

    I_CUDNT = """<i>sᴏʀʀʏ ɴᴏ ꜰɪʟᴇs ᴡᴇʀᴇ ꜰᴏᴜɴᴅ ꜰᴏʀ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛ {} 😕

ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴘᴇʟʟɪɴɢ ɪɴ ɢᴏᴏɢʟᴇ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ 😃

sᴇᴀʀᴄʜ🔍 ғᴏʀᴍᴀᴛ 👇

Pushpa 2021
Money heist S0E01

ᴏɴʟʏ ɴᴀᴍᴇ ᴏʀ ʏᴇᴀʀ ɴᴏ ᴇxᴛʀᴀ ᴡᴏʀᴅ</i>"""

    I_CUD_NT = """ɪ ᴄᴏᴜʟᴅɴ'ᴛ ꜰɪɴᴅ ᴀɴʏ ᴍᴏᴠɪᴇ ʀᴇʟᴀᴛᴇᴅ ᴛᴏ {}.
ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ꜱᴘᴇʟʟɪɴɢ ᴏɴ ɢᴏᴏɢʟᴇ ᴏʀ ɪᴍᴅʙ..."""

    MVE_NT_FND = """<i>ᴡᴇ ᴅɪᴅ ɴᴏᴛ ғɪɴᴅ ᴀɴʏ ᴍᴏᴠɪᴇ ᴡɪᴛʜ ᴛʜɪs ɴᴀᴍᴇ 🙅,

ᴛʜɪs ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ʜᴀs ʙᴇᴇɴ sᴇɴᴛ ᴛᴏ ᴛʜᴇ ᴀᴅᴍɪɴ</i>..."""

    TOP_ALRT_MSG = """sᴇᴀʀᴄʜɪɴɢ 🔍..."""

    MELCOW_ENG = """<b>Hᴇʟʟᴏ {} 😍, Aɴᴅ Wᴇʟᴄᴏᴍᴇ Tᴏ {} Gʀᴏᴜᴘ ❤️</b>"""

    

    NORSLTS = """
#NoResult
★ Gʀᴏᴜᴘ Nᴀᴍᴇ <b>: {}</b>(<code>{}</code>)
★ Tᴏᴛᴀʟ Usᴇʀs {}
★ Bᴏᴛ {}
★ Usᴇʀ <b>: {}</b>

★ Mᴇssᴀɢᴇ <code>{}</code>"""

    PMNORSLTS = """
#Pm_NoResult
★ Bᴏᴛ {}
★ Uᴇʀ <b>: {}</b>

★ Mᴇssᴀɢᴇ <code>{}</code>"""

    CAPTION = """
<b>📂 Fɪʟᴇ ɴᴀᴍᴇ : <b>{file_name} Powered By @Rkmovieszip</b>"""

    IMDB_TEMPLATE_TXT = """
<b>
🏷 Title: <a href={url}>{title}</a>
🎭 Genres: {genres}
📆 Year: <a href={url}/releaseinfo>{year}</a>
🌟 Rating: <a href={url}/ratings>{rating}</a> / 10</b> """
    
    CHANNELS = """
<b>ᴊᴏɪɴ ᴛʜɪs ᴄʜᴀɴɴᴇʟ ғᴏʀ ʀᴇᴘᴏ ᴜᴘᴅᴀᴛᴇs </b>"""
    
    STATUS_TXT = """<b>    
‣ ᴛᴏᴛᴀʟ ꜰɪʟᴇꜱ : <code>{}</code>
‣ ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ : <code>{}</code>
‣ ᴛᴏᴛᴀʟ ɢʀᴏᴜᴘꜱ : <code>{}</code>
‣ ᴜꜱᴇᴅ ꜱᴛᴏʀᴀɢᴇ : <code>{}</code>
‣ ꜰʀᴇᴇ ꜱᴛᴏʀᴀɢᴇ : <code>{}</code>
</b>"""

    DISCLAIMER_TXT = """
<b>ᴛʜɪꜱ ɪꜱ ᴀɴ ᴏᴘᴇɴ ꜱᴏᴜʀᴄᴇ ᴘʀᴏᴊᴇᴄᴛ.

ᴀʟʟ ᴛʜᴇ ꜰɪʟᴇꜱ ɪɴ ᴛʜɪꜱ ʙᴏᴛ ᴀʀᴇ ꜰʀᴇᴇʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ᴏɴ ᴛʜᴇ ɪɴᴛᴇʀɴᴇᴛ ᴏʀ ᴘᴏꜱᴛᴇᴅ ʙʏ ꜱᴏᴍᴇʙᴏᴅʏ ᴇʟꜱᴇ. ᴊᴜꜱᴛ ꜰᴏʀ ᴇᴀꜱʏ ꜱᴇᴀʀᴄʜɪɴɢ ᴛʜɪꜱ ʙᴏᴛ ɪꜱ ɪɴᴅᴇxɪɴɢ ꜰɪʟᴇꜱ ᴡʜɪᴄʜ ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ᴜᴘʟᴏᴀᴅᴇᴅ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ. ᴡᴇ ʀᴇꜱᴘᴇᴄᴛ ᴀʟʟ ᴛʜᴇ ᴄᴏᴘʏʀɪɢʜᴛ ʟᴀᴡꜱ ᴀɴᴅ ᴡᴏʀᴋꜱ ɪɴ ᴄᴏᴍᴘʟɪᴀɴᴄᴇ ᴡɪᴛʜ ᴅᴍᴄᴀ ᴀɴᴅ ᴇᴜᴄᴅ. ɪꜰ ᴀɴʏᴛʜɪɴɢ ɪꜱ ᴀɢᴀɪɴꜱᴛ ʟᴀᴡ ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ꜱᴏ ᴛʜᴀᴛ ɪᴛ ᴄᴀɴ ʙᴇ ʀᴇᴍᴏᴠᴇᴅ ᴀꜱᴀᴘ. ɪᴛ ɪꜱ ꜰᴏʀʙɪʙʙᴇɴ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ, ꜱᴛʀᴇᴀᴍ, ʀᴇᴘʀᴏᴅᴜᴄᴇ, ꜱʜᴀʀᴇ ᴏʀ ᴄᴏɴꜱᴜᴍᴇ ᴄᴏɴᴛᴇɴᴛ ᴡɪᴛʜᴏᴜᴛ ᴇxᴘʟɪᴄɪᴛ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ꜰʀᴏᴍ ᴛʜᴇ ᴄᴏɴᴛᴇɴᴛ ᴄʀᴇᴀᴛᴏʀ ᴏʀ ʟᴇɢᴀʟ ᴄᴏᴘʏʀɪɢʜᴛ ʜᴏʟᴅᴇʀ. ɪꜰ ʏᴏᴜ ʙᴇʟɪᴇᴠᴇ ᴛʜɪꜱ ʙᴏᴛ ɪꜱ ᴠɪᴏʟᴀᴛɪɴɢ ʏᴏᴜʀ ɪɴᴛᴇʟʟᴇᴄᴛᴜᴀʟ ᴘʀᴏᴘᴇʀᴛʏ, ᴄᴏɴᴛᴀᴄᴛ ᴛʜᴇ ʀᴇꜱᴘᴇᴄᴛɪᴠᴇ ᴄʜᴀɴɴᴇʟꜱ ꜰᴏʀ ʀᴇᴍᴏᴠᴀʟ. ᴛʜᴇ ʙᴏᴛ ᴅᴏᴇꜱ ɴᴏᴛ ᴏᴡɴ ᴀɴʏ ᴏꜰ ᴛʜᴇꜱᴇ ᴄᴏɴᴛᴇɴᴛꜱ, ɪᴛ ᴏɴʟʏ ɪɴᴅᴇx ᴛʜᴇ ꜰɪʟᴇꜱ ꜰʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ. 

🌿 ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href=https://t.me/Looterekrish>Lₒₒ𝚝ₑᵣₑ™</a>"""

    USERS_TXT = """
👇 ᴄᴏᴍᴍᴀɴᴅꜱ ʟɪꜱᴛ ғᴏʀ ᴜꜱᴇʀꜱ 👇
    
• /id - ɢᴇᴛ ɪᴅ ᴏꜰ ᴀ ꜱᴘᴇᴄɪꜰɪᴇᴅ ᴜꜱᴇʀ.
• /info  - ɢᴇᴛ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀ ᴜꜱᴇʀ.
• /imdb  - ɢᴇᴛ ᴛʜᴇ ꜰɪʟᴍ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ꜰʀᴏᴍ ɪᴍᴅʙ ꜱᴏᴜʀᴄᴇ.
• /search  - ɢᴇᴛ ᴛʜᴇ ꜰɪʟᴍ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ꜰʀᴏᴍ ᴠᴀʀɪᴏᴜꜱ ꜱᴏᴜʀᴄᴇꜱ.
• /request - sᴇɴᴅ ᴀ Mᴏᴠɪᴇ/Sᴇʀɪᴇs ʀᴇᴏ̨ᴜᴇsᴛ ᴛᴏ ʙᴏᴛ ᴀᴅᴍɪɴs. ( ᴏɴʟʏ ᴡᴏʀᴋs ᴏɴ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ )
• /plans - ᴄʜᴇᴄᴋ ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀꜱʜɪᴘ ᴘʟᴀɴꜱ.
• /myplan - ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴄᴜʀʀᴜɴᴛ ᴘʟᴀɴ.
• /redeem - ʀᴇᴅᴇᴇᴍ ʙᴏᴛ ᴘʀᴇᴍɪᴜᴍ ᴄᴏᴅᴇ
• /sticker_id - ᴛᴇʟᴇɢʀᴀᴍ sᴛɪᴄᴋᴇʀ ɪᴅ
"""

    GROUP_TXT = """
👇 ᴄᴏᴍᴍᴀɴᴅꜱ ʟɪꜱᴛ ꜰᴏʀ ɢʀᴏᴜᴘ 👇
    
• /connect  - ᴄᴏɴɴᴇᴄᴛ ᴀ ᴘᴀʀᴛɪᴄᴜʟᴀʀ ᴄʜᴀᴛ ᴛᴏ ʏᴏᴜʀ ᴘᴍ.
• /disconnect  - ᴅɪꜱᴄᴏɴɴᴇᴄᴛ ꜰʀᴏᴍ ᴀ ᴄʜᴀᴛ.
• /set_verify -  sᴇᴛ ғɪʀsᴛ ᴠᴇʀɪғʏ ᴜʀʟ
• /set_verify2 - sᴇᴛ sᴇᴄᴏɴᴅ ᴠᴇʀɪғʏ ᴜʀʟ
• /set_verify3 - sᴇᴛ ᴛʜɪʀᴅ ᴠᴇʀɪғʏ ᴜʀʟ
• /verify_gap - sᴇᴛ sᴇᴄᴏɴᴅ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ɢᴀᴘ ᴛɪᴍᴇ
• /verify_gap2 - sᴇᴛ ᴛʜɪʀᴅ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ɢᴀᴘ ᴛɪᴍᴇ
• /set_tutorial - sᴇᴛ ғɪsᴛ ᴠᴇʀɪғʏ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ
• /set_tutorial_2 - sᴇᴛ sᴇᴄᴏɴᴅ ᴠᴇʀɪғʏ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ
• /set_tutorial_3 - sᴇᴛ ᴛʜɪʀᴅ ᴠᴇʀɪғʏ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ
• /set_caption - ᴄʜᴀɴɢᴇ ғɪʟᴇ ᴄᴀᴘᴛɪᴏɴ
• /set_fsub - sᴇᴛ ғsᴜʙ ᴄʜᴀɴɴᴇʟ ɪᴅ, ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ
• /remove_fsub - ʀᴇᴍᴏᴠᴇ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ᴄʜᴀɴɴᴇʟ
• /set_log - sᴇᴛ ʟᴏɢ_ᴄʜᴀɴɴᴇʟ
• /set_file_limit - sᴇᴛ ᴅᴀɪʟʏ ғɪʟᴇ ʟɪᴍɪᴛ
• /set_send_limit - sᴇᴛ sᴇᴅɴᴅ ᴀʟʟ ʙᴜᴛᴛᴏɴ ʟɪᴍɪᴛ ғᴏʀ 1ᴅᴀʏ
• /set_template - ᴄʜᴀɴɢᴇ ɪᴍᴇʙ ᴀᴜᴛᴏ ғɪʟᴛᴇʀ  ʀᴇsᴜʟᴛ ᴘᴀɢᴇ  
• /set_stream - ᴄʜᴀɴɢᴇ sᴛʀᴇᴀᴍ sʜᴏʀᴛ ʟɪɴᴋ
• /connections - ʟɪꜱᴛ ᴀʟʟ ʏᴏᴜʀ ᴄᴏɴɴᴇᴄᴛɪᴏɴꜱ.
• /settings - ᴄʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs ᴀs ʏᴏᴜʀ ᴡɪsʜ.
• /details - ᴠɪᴇᴡ ɢʀᴏᴜᴘ sᴀᴠᴇᴅ ᴠᴀʟᴜᴇ
"""

    ADMIC_TXT = """
👇 ᴄᴏᴍᴍᴀɴᴅꜱ ʟɪꜱᴛ ꜰᴏʀ ᴀᴅᴍɪɴꜱ 👇

• /add_premium - <code>ᴀᴅᴅ ᴀɴʏ ᴜꜱᴇʀ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ.</code>
• /remove_premium - <code>ʀᴇᴍᴏᴠᴇ ᴀɴʏ ᴜꜱᴇʀ ꜰʀᴏᴍ ᴘʀᴇᴍɪᴜᴍ.</code>
• /premium_users - <code>ɢᴇᴛ ʟɪꜱᴛ ᴏꜰ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ.</code>
• /get_premium - <code>ɢᴇᴛ ɪɴꜰᴏ ᴏꜰ ᴀɴʏ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ.</code>
• /restart - <code>ʀᴇꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ.</code>
• /code - ɢᴇɴᴇʀᴀᴛᴇ ʙᴏᴛ ᴘʀᴇᴍɪᴜᴍ ᴄᴏᴅᴇ
• /clearcodes - ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴄᴏᴅᴇ 
• /allcodes - ᴠɪᴇᴡ ᴀʟʟ ᴄᴏᴅᴇ ᴀɴᴅ ᴅᴇᴛᴀɪʟs
• /grp_delete - ᴅᴇʟᴇᴛᴇ ᴀʟʟ ɢʀᴏᴜᴘ ғᴏʀ ᴅᴀᴛᴀʙᴀsᴇ
• /setlink - sᴇᴛ ғǫᴅɴ ᴜʀʟ
• /set_value - set value True False in Direct Bot
"""
    ADMIC_TEX2T = """
👇 ᴄᴏᴍᴍᴀɴᴅꜱ ʟɪꜱᴛ ꜰᴏʀ ᴀᴅᴍɪɴꜱ 👇

• /logs - <code>ɢᴇᴛ ᴛʜᴇ ʀᴇᴄᴇɴᴛ ᴇʀʀᴏʀꜱ.</code>
• /delete - <code>ᴅᴇʟᴇᴛᴇ ᴀ ꜱᴘᴇᴄɪꜰɪᴄ ꜰɪʟᴇ ꜰʀᴏᴍ ᴅʙ.</code>
• /users - <code>ɢᴇᴛ ʟɪꜱᴛ ᴏꜰ ᴍʏ ᴜꜱᴇʀꜱ ᴀɴᴅ ɪᴅꜱ.</code>
• /chats - <code>ɢᴇᴛ ʟɪꜱᴛ ᴏꜰ ᴍʏ ᴄʜᴀᴛꜱ ᴀɴᴅ ɪᴅꜱ.</code>
• /leave  - <code>ʟᴇᴀᴠᴇ ꜰʀᴏᴍ ᴀ ᴄʜᴀᴛ.</code>
• /disable  -  <code>ᴅɪꜱᴀʙʟᴇ ᴀ ᴄʜᴀᴛ.</code>
• /ban  - <code>ʙᴀɴ ᴀ ᴜꜱᴇʀ.</code>
• /unban  - <code>ᴜɴʙᴀɴ ᴀ ᴜꜱᴇʀ.</code>
• /channel - <code>ɢᴇᴛ ʟɪꜱᴛ ᴏꜰ ᴛᴏᴛᴀʟ ᴄᴏɴɴᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘꜱ.</code>
• /broadcast - <code>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀꜱ.</code>
• /grp_broadcast - <code>ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ ᴄᴏɴɴᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘs.</code>
• /deletefiles - <code>ᴅᴇʟᴇᴛᴇ CᴀᴍRɪᴘ ᴀɴᴅ PʀᴇDVD ғɪʟᴇs ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ's ᴅᴀᴛᴀʙᴀsᴇ.</code>
• /deleteall - ᴅᴇʟᴇᴛᴇ ᴀʟʟ ɪɴᴅᴇxᴇs ғɪʟᴇs
• /send - <code>ꜱᴇɴᴅ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴀ ᴘᴀʀᴛɪᴄᴜʟᴀʀ ᴜꜱᴇʀ.</code>
"""
    
    PREMIUM_CMD = """<b>
💵 <i> ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs </ɪ>

1. 20₹ = 1ᴍᴏɴᴛʜ
2. 38₹ = 2ᴍᴏɴᴛʜ
3. 55₹ = 3ᴍᴏɴᴛʜ
4. 110₹ = 6ᴍᴏɴᴛʜ

==========================
🎁 <u>ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs</u> :

○ sᴇᴀʀᴄʜ ᴍᴏᴠɪᴇ ɪɴ ᴛʜᴇ ʙᴏᴛ
○ ɴᴏ ғɪʟᴇ ʟɪᴍɪᴛs
○ ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ғɪʟᴇs
○ ɴᴏ ʟɪᴍɪᴛs ғᴏʀ sᴇɴᴅ ᴀʟʟ ʙᴜᴛᴛᴏɴ
○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋꜱ
○ ɴᴏ ɴᴇᴇᴅ ᴠᴇʀɪғʏ
○ ᴅɪʀᴇᴄᴛ ғɪʟᴇs   
○ ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ 
○ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs & sᴇʀɪᴇs        

==========================
➛ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ ʙʏ ᴜꜱɪɴɢ : /myplan

‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ</b>"""

    
    UPI_TXT = """<b>   
⚜️ ᴘᴀʏ ᴀᴍᴍᴏᴜɴᴛ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ʏᴏᴜʀ ᴘʟᴀɴ ᴀɴᴅ ᴇɴᴊᴏʏ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀꜱʜɪᴘ !

💵 ᴜᴘɪ ɪᴅ - <code>rkmovieszip@ybl</code>

‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ
<i>पेमेंट होने के बाद हमे स्क्रीन शॉट भेजें</i>.</b>"""

    QR_TXT = """<b>
⚜️ ᴘᴀʏ ᴀᴍᴍᴏᴜɴᴛ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ʏᴏᴜʀ ᴘʟᴀɴ ᴀɴᴅ ᴇɴᴊᴏʏ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀꜱʜɪᴘ !


‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ
<i>पेमेंट होने के बाद हमे स्क्रीन शॉट भेजें</i>.</b>"""

    FREE_TXT = """<b>👋 ʜᴇʏ {},
    
<b>🥳 ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴꜱ

🎉 ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ꜰʀᴇᴇ ᴘʀᴇᴍɪᴜᴍ ᴛʀᴀɪʟ ꜰᴏʀ <u>5 ᴍɪɴᴜᴛᴇs 

sᴇᴀʀᴄʜ🔍 ᴍᴏᴠɪᴇ ᴀɢᴀɪɴ</u> ꜰʀᴏᴍ ɴᴏᴡ !</b>"""
    
    
    NOT_AVAILABLE_TXT = """{}

ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛᴇᴅ ᴄᴏɴᴛᴇɴᴛ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ"""

    SERIES_FORMAT_TXT = """{}
    
ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ғᴏʀᴍᴀᴛ ᴡʀᴏɴɢ❌ 
ғᴏʟʟᴏᴡ ᴛʜɪs ғᴏʀᴍᴀᴛ 👇

Money heist S01E01
Money heist S01"""

    UPLOADED_TXT = """{}
    
ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛᴇᴅ ᴄᴏɴᴛᴇɴᴛ ᴜᴘʟᴏᴀᴅᴇᴅ ✅
sᴇᴀʀᴄʜ 🔍 ᴀɢᴀɪɴ ᴀɴᴅ ɪɴᴊᴏʏ"""

    NOT_RELEASE_TXT = """{} 
    
ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛᴇᴅ ᴄᴏɴᴛᴇɴᴛ ɴᴏᴛ ʀᴇʟᴇᴀsᴇ 
ᴘʟᴇᴀsᴇ🙏 ᴡᴀɪᴛ ᴛʜᴇ ʀᴇʟᴇᴀsᴇ ᴅᴀʏ"""

    SPELL_TXT = """{} 
ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛᴇᴅ ᴄᴏɴᴛᴇɴᴛ ɴᴀᴍᴇ ɴᴏᴛ ᴍᴀᴛᴄʜ ᴀɴʏ sᴇʀɪᴇs ᴏʀ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ 

ᴘʟᴇᴀsᴇ ʀᴇǫᴜᴇsᴛ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ"""
    
    
    BROADCAST = """<u>{}</u>

Total: `{}`
Remaining: `{}`
Success: `{}`
Failed: `{}`"""

    RESTART_TXT = """
<b>Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ !

🤖 Bᴏᴛ : <a href=https://t.me/{}>{}</a>
📅 Dᴀᴛᴇ : <code>{}</code>
⏰ Tɪᴍᴇ : <code>{}</code>
🌐 Tɪᴍᴇᴢᴏɴᴇ : <code>Asia/Kolkata</code>
🛠️ Bᴜɪʟᴅ Sᴛᴀᴛᴜs: <code>v2.7.1 [ Sᴛᴀʙʟᴇ ]</code></b>"""

    LOGO = """
██╗       ██████╗  ██████╗ ████████╗███████╗██████╗ ███████╗
██║      ██╔═══██╗██╔═══██╗╚══██╔══╝██╔════╝██╔══██╗██╔════╝
██║      ██║   ██║██║   ██║   ██║   █████╗  ██████╔╝█████╗  
██║      ██║   ██║██║   ██║   ██║   ██╔══╝  ██╔══██╗██╔══╝  
███████╗ ╚██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║███████╗
╚══════╝  ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝
                                                     
BOT SUCCESSFULLY STARTED 💥 ✅✅✅✅✅✅✅✅✅"""                                                                                  
