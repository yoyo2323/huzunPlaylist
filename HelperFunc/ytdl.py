# HuzunluArtemis - 2021 (Licensed under GPL-v3)

import logging

from yt_dlp.utils import UnavailableVideoError
from HelperFunc.clean import cleanFiles
from HelperFunc.progressMulti import ReadableTime, TimeFormatter, humanbytes
from pyrogram.types.messages_and_media.message import Message
import os, time, math
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)
from config import Config
from yt_dlp import YoutubeDL, DownloadError

SAVE_PATH = "musics"

videoCount = None
infoMes = None
mesaj = None
last_downloaded = 0
downloaded_bytes = 0
progress = 0.0
toplamBoyut = 0
indirilen = 1
startTime = time.time()

def ExitWithException(message:Message, exception:str, link:str):
    mes = None
    if "is not a valid URL." in str(exception):
        mes = f"🇬🇧 not a valid link 🇹🇷 geçersiz link:\n`{link}`"
    if not mes: mes = f"`{str(exception)}`"
    mes += "\n\n🇬🇧 click and read: /help\n🇹🇷 tıkla ve oku: /yardim"
    message.edit_text(mes,disable_web_page_preview=True)
    clearVars()
    cleanFiles()

def clearVars():
    global mesaj,last_downloaded,downloaded_bytes,progress,toplamBoyut,indirilen, infoMes, startTime, videoCount
    mesaj = None
    videoCount = None
    infoMes = None
    last_downloaded = 0
    downloaded_bytes = 0
    progress = 0.0
    toplamBoyut = 0
    indirilen = 1
    startTime = time.time()

class YtdlLogger(object):
    def debug(self, msg):
        #LOGGER.debug(f"YtdlLogger - {msg}")
        pass

    def warning(self, msg):
        LOGGER.warning(f"YtdlLogger - {msg}")

    def error(self, msg):
        LOGGER.error(f"YtdlLogger - {msg}")

def progress_for_ytdl(
    current,
    total,
    start
):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:
    #if round(current / total * 100, 0) % 5 == 0:
        try: percentage = current * 100 / total
        except ZeroDivisionError: percentage = 0
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
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
        return progress + Config.PROGRESS.format(
            round(percentage, 2), # Percent
            humanbytes(total), # Total Size
            humanbytes(current), # Finished Size
            humanbytes(total-current), # Remaining Size
            humanbytes(speed), # Speed
            estimated_total_time if estimated_total_time != '' else "0 s", # Estimated Time
            time_to_completion if time_to_completion != '' else "0 s", # Remaining Time
            elapsed_time if elapsed_time != '' else "0 s", # Passed time
            ReadableTime(time.time() - Config.botStartTime)
        ) + progressReverse 
    else: return None

def progressHook(d):
    global mesaj, downloaded_bytes,last_downloaded,indirilen,progress, startTime, videoCount, infoMes
    if d['status'] == 'finished':
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        last_downloaded += os.path.getsize(d['filename'])
        indirilen = indirilen + 1
        LOGGER.info("Downloaded {}".format(file_tuple[1]))
    if d['status'] == 'error':
        LOGGER.error(f"progressHook - Error when download: {d['filename']}")
    if d['status'] == 'downloading':
        downloaded_bytes = last_downloaded + d['downloaded_bytes']
        try:
            progress = (downloaded_bytes / toplamBoyut) * 100
        except ZeroDivisionError:
            progress = 0
        cp = progress_for_ytdl(downloaded_bytes, toplamBoyut, startTime)
        if cp:
            toedit = infoMes
            toedit += f"\n\nŞu an / At now:\n\n`- Sıra / Quee: {str(indirilen)}/{str(videoCount)}" + \
                "\n- İnen / Downloading: " + os.path.split(os.path.abspath(d['filename']))[1] + \
                "\n- Yüzde / Percent: " + d['_percent_str'] + \
                "\n- Kalan / Remaining: " + d['_eta_str'] + \
                "\n- Hız / Speed: " + d['_speed_str'] + \
                "\n- Boyut / Size: " + d['_total_bytes_str'] + f"`\n\nToplam / Total:\n`{cp}`" + \
                f"\n💎 @{Config.CHANNEL_OR_CONTACT}"
            toedit = toedit.format(ReadableTime(time.time() - Config.botStartTime))
            try: mesaj.edit_text(toedit, disable_web_page_preview=True)
            except: pass

def ytdDownload(link, message:Message, info:str):
    global mesaj, startTime, infoMes
    infoMes = info
    startTime = time.time()
    mesaj = message
    try:
        downloaderOptions = {
            'format': Config.YTDL_DOWNLOAD_FORMAT,
            'no_warnings': False,
            'ignoreerrors': True,
            # 'skip_unavailable_fragments': True,
            'writethumbnail': True,
            'nocheckcertificate': True,
            'outtmpl': os.path.join(SAVE_PATH, "%(title)s.%(ext)s"),
            'progress_hooks': [progressHook],
            'logger': YtdlLogger(),
            'postprocessors': [
                {
                'key': 'FFmpegExtractAudio'
                },
                {
                'key': 'FFmpegMetadata',
                'add_chapters': True,
                'add_metadata': True
                },
                {
                'key': 'EmbedThumbnail'
                }
            ]
        }
        ydl:YoutubeDL = YoutubeDL(downloaderOptions)
        ydl.download([link])
    except DownloadError as e:
        ExitWithException(mesaj, str(e), link)
        return
    except ValueError as v:
        ExitWithException(mesaj, str(v), link)
        return


def getVideoDetails(url:str, message:Message):
    global toplamBoyut, mesaj, videoCount
    mesaj = message
    ydl_opts = {
        'format': Config.YTDL_DOWNLOAD_FORMAT,
        'nocheckcertificate': True,
        # 'skip_unavailable_fragments': True,
        'ignoreerrors': True
    }
    ydl:YoutubeDL = YoutubeDL(ydl_opts)
    result = None
    try: result = ydl.extract_info(url, download=False) #We just want to extract the info
    except UnavailableVideoError as y:
        LOGGER.error(f"getVideoDetails - UnavailableVideoError: {str(y)}")
    except Exception as t: LOGGER.error(f"getVideoDetails - Exception: {str(t)}")
    videolar = []
    if 'entries' in result:
        video = result['entries']
        for i, item in enumerate(video):
            if not result['entries'][i]: continue # not available videos
            videolar.append([
                'playlist',
                str(result['entries'][i]['id']),
                str(result['entries'][i]['title']),
                str(result['entries'][i]['filesize']),
                str(result['entries'][i]['upload_date']),
                str(result['entries'][i]['duration_string']),
                str(result['entries'][i]['webpage_url']),
                str(result['entries'][i]['uploader']),
                str(result['entries'][i]['container']),
                str(result['entries'][i]['format']),
                str(result['entries'][i]['format_id']),
                str(result['entries'][i]['acodec']),
                str(result['entries'][i]['playlist_title']),
                str(result['entries'][i]['playlist_id']),
                str(result['entries'][i]['playlist_index']),
                str(result['entries'][i]['n_entries'])
            ])
    else:
        videolar.append([
            'video',
            str(result['id']),
            str(result['title']),
            str(result['filesize']),
            str(result['upload_date']),
            str(result['duration_string']),
            str(result['webpage_url']),
            str(result['uploader']),
            str(result['container']),
            str(result['format']),
            str(result['format_id']),
            str(result['acodec'])
        ])
    
    kendisi = []
    try: kendisi.append(str(result['id']))
    except: kendisi.append(None)
    try: kendisi.append(str(result['channel_id']))
    except: kendisi.append(None)
    try: kendisi.append(str(result['title']))
    except: kendisi.append(None)
    try: kendisi.append(str(result['channel']))
    except: kendisi.append(None)
    try: kendisi.append(str(result['channel_url']))
    except: kendisi.append(None)
    try: kendisi.append(str(result['webpage_url']))
    except: kendisi.append(None)
    videoCount = len(videolar)
    for x in range(len(videolar)): toplamBoyut = toplamBoyut + int(videolar[x][3])
    return videolar, kendisi

