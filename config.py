# HuzunluArtemis - 2021 (Licensed under GPL-v3)

import logging, os, time
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class Config(object):
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "") # dont touch
    
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", 'HuzunluArtemis')
    CHANNEL_OR_CONTACT = os.environ.get("CHANNEL_OR_CONTACT", 'HuzunluArtemis')
    FINISHED_PROGRESS_STR = os.environ.get('FINISHED_PROGRESS_STR','●')
    UN_FINISHED_PROGRESS_STR = os.environ.get('UN_FINISHED_PROGRESS_STR','○')
    PROGRESS = "🔥 Biten Yüzde / Percent: % {0}\n📀 Toplam Boyut / Total Size: {1}\n📤 Biten Boyut / Finished: {2}\n" + \
        "📥 Kalan Boyut / Remaining: {3}\n⚡️ Anlık Hız / Speed: {4}/s\n⏳ Tahmini Süre / Estimated: {5}\n⏰ Kalan Süre / Remaining: {6}\n⌛️ Geçen Süre / Passed: {7}"
    PROGRESSBAR_LENGTH = int(os.environ.get('PROGRESSBAR_LENGTH', 25))
    JOIN_CHANNEL_STR = os.environ.get('JOIN_CHANNEL_STR',
        "Merhaba / Hi {}\n\n" + \
        "🇬🇧 First subscribe my channel from button, then send /start again.\n" + \
        "🇹🇷 Önce butondan kanala abone ol, sonra bana /start yaz.")
    YOU_ARE_BANNED_STR = os.environ.get('YOU_ARE_BANNED_STR',
        "🇬🇧 You are Banned to use me.\n🇹🇷 Banlanmışsın ezik.\n\nDestek / Support: {}")
    JOIN_BUTTON_STR = os.environ.get('JOIN_BUTTON_STR', "🇬🇧 Join / 🇹🇷 Katıl")
    OWNER_ID = int(os.environ.get('OWNER_ID', 0)) # give your owner id # if given 0 shell will not works
    AUTH_IDS = [int(x) for x in os.environ.get("AUTH_IDS", "0").split()] # if open to everyone give 0
    PREMIUM_USERS = [int(x) for x in os.environ.get("PREMIUM_USERS", "0").split()] # quee not affect by premium
    # forcesub vars
    FORCE_SUBSCRIBE_CHANNEL = os.environ.get('FORCE_SUBSCRIBE_CHANNEL', '') # force subscribe channel link.
    if FORCE_SUBSCRIBE_CHANNEL == "" or FORCE_SUBSCRIBE_CHANNEL == " " or FORCE_SUBSCRIBE_CHANNEL == None: FORCE_SUBSCRIBE_CHANNEL = None # bu satıra dokunmayın.
    # commands
    SESSION = os.environ.get('SESSION', 'PlaylistAudioBot')
    LOG_COMMAND = [os.environ.get('LOG_COMMAND','log')]
    STATS_COMMAND = [os.environ.get('STATS_COMMAND','stats')]
    TG_SPLIT_SIZE = int(os.environ.get("TG_SPLIT_SIZE", "2097151000"))
    MUSIC_COMMAND = [os.environ.get('MUSIC_COMMAND','music')]
    RESTART_COMMAND = [os.environ.get('RESTART_COMMAND','restart')]
    SHELL_COMMAND = [os.environ.get('SHELL_COMMAND','shell')]
    FLAME_URL = os.environ.get('FLAME_URL','https://github.com/HuzunluArtemis/PlaylistAudioBot')
    PING_COMMAND = [os.environ.get('PING_COMMAND','ping')]
    YTDL_DOWNLOAD_FORMAT = os.environ.get('YTDL_DOWNLOAD_FORMAT', 'bestaudio[ext=m4a] / bestaudio')
    botStartTime = time.time() # dont touch
    UPDATE_YTDL_EVERY_DOWNLOAD = str(os.environ.get("UPDATE_YTDL_EVERY_DOWNLOAD", "True")).lower() == 'true'
    UPDATE_REQUIREMETS_EVERY_RESTART = str(os.environ.get("UPDATE_REQUIREMETS_EVERY_RESTART", "True")).lower() == 'true'
    SEND_LOGS_WHEN_DYING = str(os.environ.get("SEND_LOGS_WHEN_DYING", "False")).lower() == 'true'
    SLEEP_BETWEEN_SEND_FILES = int(os.environ.get("SLEEP_BETWEEN_SEND_FILES", 7))
    VIDEO_LIMIT_FREE_USER = int(os.environ.get("VIDEO_LIMIT_FREE_USER", 0))
    SIZE_LIMIT_FREE_USER = int(os.environ.get("SIZE_LIMIT_FREE_USER", 0))
    VIDEO_LIMIT_PREMIUM_USER = int(os.environ.get("VIDEO_LIMIT_PREMIUM_USER", 0))
    SIZE_LIMIT_PREMIUM_USER = int(os.environ.get("SIZE_LIMIT_PREMIUM_USER", 0))
    PROCESS_PER_USER_PREMIUM_USER = int(os.environ.get('PROCESS_PER_USER_PREMIUM_USER', '0'))
    PROCESS_PER_USER_FREE_USER = int(os.environ.get('PROCESS_PER_USER_FREE_USER', '2'))
    SORT_UPLOAD = str(os.environ.get("SORT_UPLOAD", "MetadataChange")).lower() #
    normalValues = ['contentmodification', 'normalsort', 'naturalsort', 'metadatachange', 'reversesort']
    if not SORT_UPLOAD in normalValues:
        LOGGER.error("Please enter valid sorting algorithm. See Config file. Using default value now.")
        SORT_UPLOAD = 'metadatachange'
    HELP_COMMANDS = ["start", "help", "about", "yardım", "h", "y"]
    if OWNER_ID != 0:
        AUTH_IDS.append(OWNER_ID)
        PREMIUM_USERS.append(OWNER_ID)
    if not BOT_USERNAME.startswith('@'): BOT_USERNAME = '@' + BOT_USERNAME # bu satıra dokunmayın.
    # komutları kopyala
    AllCom = [LOG_COMMAND,HELP_COMMANDS, PING_COMMAND, MUSIC_COMMAND, SHELL_COMMAND, STATS_COMMAND, RESTART_COMMAND]
    for ComS in AllCom:
        Lier = ComS.copy()
        for p in Lier:
            ComS.append(p+BOT_USERNAME)
    # komutları kopyala
