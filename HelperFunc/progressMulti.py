# HuzunluArtemis - 2021 (Licensed under GPL-v3)

"""
usage:
make this vars

downloadedSize = get_size(outDir)
totalSent = 0

and add sent file's size to totalSent in every sent file.
(totalSent = totalSent + os.path.getsize(dosyaYolu))
see musicDown.py 115

if you find better way, pr
"""

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)
import math, time
from config import Config

async def progressMulti(
    current,
    total,
    ud_type,
    message,
    start,
    realTotal,
    realDownloaded
):
    current = realDownloaded + current
    now = time.time()
    diff = now - start
    # if round(current / total * 100, 0) % 10 == 0:
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / realTotal
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((realTotal - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        time_to_completion = TimeFormatter(milliseconds=time_to_completion)
        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "\n💦 [{0}{1}]\n".format(
            ''.join([Config.FINISHED_PROGRESS_STR for i in range(math.floor(percentage / (100/Config.PROGRESSBAR_LENGTH)))]),
            ''.join([Config.UN_FINISHED_PROGRESS_STR for i in range(Config.PROGRESSBAR_LENGTH - math.floor(percentage / (100/Config.PROGRESSBAR_LENGTH)))])
            )
        progressReverse = "\n💦 [{1}{0}]\n".format(
            ''.join([Config.FINISHED_PROGRESS_STR for i in range(math.floor(percentage / (100/Config.PROGRESSBAR_LENGTH)))]),
            ''.join([Config.UN_FINISHED_PROGRESS_STR for i in range(Config.PROGRESSBAR_LENGTH - math.floor(percentage / (100/Config.PROGRESSBAR_LENGTH)))])
            )
        tmp = progress + Config.PROGRESS.format(
            round(percentage, 2), # Percent
            humanbytes(realTotal), # Total Size
            humanbytes(current), # Finished Size
            humanbytes(realTotal-current), # Remaining Size
            humanbytes(speed), # Speed
            estimated_total_time if estimated_total_time != '' else "0 s", # Estimated Time
            time_to_completion if time_to_completion != '' else "0 s", # Remaining Time
            elapsed_time if elapsed_time != '' else "0 s", # Passed time
            ReadableTime(time.time() - Config.botStartTime)
        ) + progressReverse 
        try:
            await message.edit(text=f"{ud_type}\n`{tmp}`" + f"\n💎 @{Config.CHANNEL_OR_CONTACT}")
        except:
            pass


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + "B"


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

def ReadableTime(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result