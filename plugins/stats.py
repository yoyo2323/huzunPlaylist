# HuzunluArtemis - 2021 (Licensed under GPL-v3)

from pyrogram import Client, filters
from HelperFunc.messageFunc import sendMessage
from HelperFunc.authUserCheck import AuthUserCheckSync
from HelperFunc.forceSubscribe import ForceSubSync
from config import Config
import psutil
import shutil
import logging
import time
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

from HelperFunc.progressMulti import humanbytes, ReadableTime

@Client.on_message(filters.command(Config.STATS_COMMAND))
def stats(client, message):
    if not AuthUserCheckSync(message): return
    if ForceSubSync(client, message) == 400: return
    try:
        total, used, free = shutil.disk_usage('.')
        total = humanbytes(total)
        used = humanbytes(used)
        free = humanbytes(free)
        sent = humanbytes(psutil.net_io_counters().bytes_sent)
        recv = humanbytes(psutil.net_io_counters().bytes_recv)
        cpuUsage = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        stats = f'<b>Bot Uptime:</b> <code>{ReadableTime(time.time() - Config.botStartTime)}</code>\n' \
            f'<b>Total Disk Space:</b> <code>{total}</code>\n' \
            f'<b>Used:</b> <code>{used}</code> ' \
            f'<b>Free:</b> <code>{free}</code>\n\n' \
            f'<b>Upload:</b> <code>{sent}</code>\n' \
            f'<b>Download:</b> <code>{recv}</code>\n\n' \
            f'<b>CPU:</b> <code>{cpuUsage}%</code> ' \
            f'<b>RAM:</b> <code>{memory}%</code> ' \
            f'<b>DISK:</b> <code>{disk}%</code>\n\n'
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
		f"🌿 Quee Limit / Sıra Limiti: {str(QueeLim)}\n🥕 Video Limit / Video Limiti: {str(vidLim)}"
        sendMessage(message,stats)
    except Exception as e:
        sendMessage(message,"🇬🇧 Maybe your shell message was empty.\n🇹🇷 Boş bir şeyler döndü valla.")
        LOGGER.error(str(e))
