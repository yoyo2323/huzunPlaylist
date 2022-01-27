# HuzunluArtemis - 2021 (Licensed under GPL-v3)

from pyrogram import Client, filters
from HelperFunc.messageFunc import sendMessage
from HelperFunc.authUserCheck import AuthUserCheckSync
from HelperFunc.forceSubscribe import ForceSubSync
from HelperFunc.randomUserAgent import getRandomUserAgent
from config import Config
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters
import logging, requests, subprocess
from time import time
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

from HelperFunc.progressMulti import humanbytes, ReadableTime


def getHerokuDetails(h_api_key, h_app_name):
    try: import heroku3
    except ModuleNotFoundError: subprocess.run("pip install heroku3", capture_output=False, shell=True)
    try: import heroku3
    except Exception as f:
        LOGGER.warning("heroku3 cannot imported. add to your deployer requirements.txt file.")
        LOGGER.warning(f)
        return None
    if (not h_api_key) or (not h_app_name): return None
    try:
        heroku_api = "https://api.heroku.com"
        Heroku = heroku3.from_key(h_api_key)
        app = Heroku.app(h_app_name)
        useragent = getRandomUserAgent()
        user_id = Heroku.account().id
        headers = {
            "User-Agent": useragent,
            "Authorization": f"Bearer {h_api_key}",
            "Accept": "application/vnd.heroku+json; version=3.account-quotas",
        }
        path = "/accounts/" + user_id + "/actions/get-quota"
        session = requests.Session()
        result = (session.get(heroku_api + path, headers=headers)).json()
        abc = ""
        account_quota = result["account_quota"]
        quota_used = result["quota_used"]
        quota_remain = account_quota - quota_used
        abc += f"Account: {ReadableTime(account_quota)} | "
        abc += f"Used: {ReadableTime(quota_used)} | "
        abc += f"Free: {ReadableTime(quota_remain)}\n"
        # App Quota
        AppQuotaUsed = 0
        OtherAppsUsage = 0
        for apps in result["apps"]:
            if str(apps.get("app_uuid")) == str(app.id):
                try:
                    AppQuotaUsed = apps.get("quota_used")
                except Exception as t:
                    LOGGER.error("error when adding main dyno")
                    LOGGER.error(t)
                    pass
            else:
                try:
                    OtherAppsUsage += int(apps.get("quota_used"))
                except Exception as t:
                    LOGGER.error("error when adding other dyno")
                    LOGGER.error(t)
                    pass
        abc += f"Usage {app.name}: {ReadableTime(AppQuotaUsed)}"
        abc += f" | Other Apps: {ReadableTime(OtherAppsUsage)}"
        return abc
    except Exception as g:
        LOGGER.error(g)
        return None


@Client.on_message(filters.command(Config.STATS_COMMAND))
def stats(client, message):
    if not AuthUserCheckSync(message): return
    if ForceSubSync(client, message) == 400: return
    try:
        currentTime = ReadableTime(time() - Config.botStartTime)
        total, used, free, disk= disk_usage('/')
        total = humanbytes(total)
        used = humanbytes(used)
        free = humanbytes(free)
        sent = humanbytes(net_io_counters().bytes_sent)
        recv = humanbytes(net_io_counters().bytes_recv)
        cpuUsage = cpu_percent(interval=0.5)
        p_core = cpu_count(logical=False)
        t_core = cpu_count(logical=True)
        swap = swap_memory()
        swap_p = swap.percent
        swap_t = humanbytes(swap.total)
        swap_u = humanbytes(swap.used)
        swap_f = humanbytes(swap.free)
        memory = virtual_memory()
        mem_p = memory.percent
        mem_t = humanbytes(memory.total)
        mem_a = humanbytes(memory.available)
        mem_u = humanbytes(memory.used)
        stats = f'<b>Bot Uptime:</b> {currentTime}\n'\
            f'<b>Disk:</b> {total} | <b>Used:</b> {used} | <b>Free:</b> {free}\n' \
            f'<b>Memory:</b> {mem_t} | <b>Used:</b> {mem_u} | <b>Free:</b> {mem_a}\n' \
            f'<b>Cores:</b> {t_core} | <b>Physical:</b> {p_core} | <b>Logical:</b> {t_core - p_core}\n' \
            f'<b>SWAP:</b> {swap_t} | <b>Used:</b> {swap_u}% | <b>Free:</b> {swap_f}\n'\
            f'<b>DISK:</b> {disk}% | <b>RAM:</b> {mem_p}% | <b>CPU:</b> {cpuUsage}% | | <b>SWAP:</b> {swap_p}%\n' \
            f'<b>Total Upload:</b> {sent} | <b>Total Download:</b> {recv}\n\n'
        plan = None
        sizeLim = 0
        QueeLim = 0
        vidLim = 0
        if not message.from_user.id in Config.PREMIUM_USERS:
            sizeLim = Config.SIZE_LIMIT_FREE_USER
            QueeLim = Config.PROCESS_PER_USER_FREE_USER
            vidLim = Config.VIDEO_LIMIT_FREE_USER
            plan = "Standart"
        else:
            sizeLim = Config.SIZE_LIMIT_PREMIUM_USER
            QueeLim = Config.PROCESS_PER_USER_PREMIUM_USER
            vidLim = Config.VIDEO_LIMIT_PREMIUM_USER
            plan = "Premium"
        if vidLim == 0: vidLim = "Sınırsız / Unlimited"
        if QueeLim == 0: QueeLim = "Sınırsız / Unlimited"
        if sizeLim == 0: sizeLim = "Sınırsız / Unlimited"
        else: sizeLim = humanbytes(sizeLim)
        stats += f"🌈 Plan: {plan}\n🔑 Size Limit / Boyut Limiti: {sizeLim}\n" + \
		f"🌿 Quee Limit / Sıra Limiti: {str(QueeLim)}\n🥕 Video Limit / Video Limiti: {str(vidLim)}\n\n"
        heroku = getHerokuDetails(Config.HEROKU_API_KEY, Config.HEROKU_APP_NAME)
        if heroku: stats += heroku
        sendMessage(message,stats)
    except Exception as e:
        sendMessage(message,"🇬🇧 Maybe your shell message was empty.\n🇹🇷 Boş bir şeyler döndü valla.")
        LOGGER.error(str(e))
