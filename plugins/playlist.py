# HuzunluArtemis - 2021 (Licensed under GPL-v3)

import time
from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message
from pyrogram.errors import FloodWait, RPCError

import logging, os
from HelperFunc.authUserCheck import AuthUserCheckSync
from HelperFunc.clean import cleanFiles
from natsort import natsorted
from HelperFunc.forceSubscribe import ForceSubSync
from HelperFunc.mediaInfo import get_media_info
from HelperFunc.progressMulti import ReadableTime, humanbytes
from HelperFunc.progressMulti import progressMulti
from HelperFunc.ytdl import clearVars, getVideoDetails, ytdDownload
from config import Config
from HelperFunc.folderSize import get_size
from HelperFunc.updatePackage import updatePipPackage
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@Client.on_message(filters.command(Config.MUSIC_COMMAND))
def playlist(client: Client, message: Message):
	if not AuthUserCheckSync(message): return
	if ForceSubSync(client, message) == 400: return
	VIDEO_SUFFIXES = ("MKV", "MP4", "MOV", "WMV", "3GP", "MPG", "WEBM", "AVI", "FLV", "M4V", "GIF")
	AUDIO_SUFFIXES = ("MP3", "M4A", "M4B", "FLAC", "WAV", "AIF", "OGG", "AAC", "DTS", "MID", "AMR", "MKA")
	IMAGE_SUFFIXES = ("JPG", "JPX", "PNG", "WEBP", "CR2", "TIF", "BMP", "JXR", "PSD", "ICO", "HEIC", "JPEG")
	outDir = "musics"
	url = ""
	if not os.path.exists(outDir): os.makedirs(outDir)

	if not message.reply_to_message:
		url = message.text.split(' ', 1)
		try:
			url = url[1]
		except IndexError:
			message.reply(f"🇬🇧 click and read: /help\n🇹🇷 tıkla ve oku: /yardim", quote=True)
			return
	else:
		url = message.reply_to_message.text
	info = f"{message.from_user.mention()} (`{str(message.from_user.id)}`)\nlink: `{url}`\n\n"
	text = info + "🇹🇷 inceleniyor.\nbu işlem her video için 1 saniye demektir.\neğer 60 videonuz varsa, 60 saniye bekleyin.\n\n"
	text += "🇬🇧 i am looking for you.\nthis means 1 second for each video.\nif you have 60 videos, wait 60 seconds.\n"
	indiriliyor: Message = message.reply(text, quote=True)
	updatePipPackage("yt-dlp")

	# calisma kontrolu
	if os.path.exists('calisiyor.txt'):
		message.reply(f"🇹🇷 elleme beni işim var.\n🇬🇧 dont touch me. i am working.\n\n" + \
		f'<a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a>', quote=True)
		return
	with open('calisiyor.txt', 'w') as writefile: writefile.write("ok")
	# calisma kontrolu

	urele, boyut, titol, uploader = getVideoDetails(url)

	#video limit
	if (Config.VIDEO_LIMIT != 0) and (len(boyut) > Config.VIDEO_LIMIT):
		try: indiriliyor.edit_text(f"🇹🇷 🇬🇧 video limit: {str(Config.VIDEO_LIMIT)}\n"
			f"🇬🇧 Yours / 🇹🇷 Seninki: {len(boyut)}"
		)
		except Exception as h: LOGGER.info(str(h))
		clearVars()
		cleanFiles()
		return

	# size limit
	toplamBoyut = 0
	for x in range(len(boyut)): toplamBoyut = toplamBoyut + int(boyut[x])
	if (Config.SIZE_LIMIT != 0) and (toplamBoyut > Config.SIZE_LIMIT):
		try: indiriliyor.edit_text(f"🇬🇧 Size limit 🇹🇷 Boyut limiti: {str(humanbytes(Config.SIZE_LIMIT))}\n" + \
			f"🇬🇧 Yours / 🇹🇷 Seninki: {humanbytes(toplamBoyut)}"
		)
		except Exception as h: LOGGER.info(str(h))
		clearVars()
		cleanFiles()
		return
	
	try: indiriliyor.edit_text(f"🇹🇷 indirilecek 🇬🇧 will down: {humanbytes(int(toplamBoyut))}")
	except: pass
	indirmeBasladi = time.time()
	ytdDownload(url, indiriliyor, info)
	indirmeBitti = time.time()
	LOGGER.info(url)
	toup = natsorted(os.listdir(outDir))
	for filo in toup:
		if filo.upper().endswith(IMAGE_SUFFIXES) or filo.upper().endswith(VIDEO_SUFFIXES):
			os.remove(os.path.join(outDir, filo))
	toup = natsorted(os.listdir(outDir))
	
	LOGGER.info("#toup: " + ", ".join(toup))
	toplamarsiv = str(len(toup))
	indirilenBoyut = get_size(outDir)
	try: indiriliyor.edit_text(f"🇹🇷 toplam inen 🇬🇧 total down: {humanbytes(int(indirilenBoyut))}")
	except: pass
	
	c_time = time.time()
	suan = 0
	toplamGonderilen = 0
	for filo in toup:
		suan = suan + 1
		kepsin = f'<a href="{Config.FLAME_URL}">🔥</a> {filo}'
		dosyaYolu = os.path.join(outDir, filo)
		if os.path.getsize(dosyaYolu) > Config.TG_SPLIT_SIZE:
			message.reply(f"büyük dosya\ntg size limit:\n\n{filo}", quote=True)
			continue
		if filo.upper().endswith(AUDIO_SUFFIXES):
			duration , artist, title = get_media_info(dosyaYolu)
			if not title: title = filo
			try:
				indiriliyor.reply_audio(audio=dosyaYolu, disable_notification=True,
				caption=kepsin,duration=duration, performer=artist,title=title, thumb="src/file.jpg",
				quote=True, progress = progressMulti,
				progress_args=(f"mesaj: {indiriliyor.link}\n" + \
				f"anlık sıra / file quee: {str(suan)}/{toplamarsiv}\n" + \
				f"yüklenen / uploading:\n`{filo}`", indiriliyor, c_time, indirilenBoyut, toplamGonderilen))
				time.sleep(Config.SLEEP_BETWEEN_SEND_FILES)
			except FloodWait as f:
				LOGGER.info("Dosya gönderimi / timesleep" + str(f))
				time.sleep(f.x * 1.5)
				indiriliyor.reply_audio(audio=dosyaYolu, disable_notification=True,
				caption=kepsin,duration=duration, performer=artist,title=title, thumb="src/file.jpg",
				quote=True, progress = progressMulti,
				progress_args=(f"mesaj: {indiriliyor.link}\n" + \
				f"anlık sıra / file quee: {str(suan)}/{toplamarsiv}\n" + \
				f"yüklenen / uploading:\n`{filo}`", indiriliyor, c_time, indirilenBoyut, toplamGonderilen))
				time.sleep(Config.SLEEP_BETWEEN_SEND_FILES)
			except RPCError as e:
				LOGGER.error("RPCError: " + str(e))
			except Exception as e:
				LOGGER.error("Exception:" + str(e))
				message.reply(f"birşeyler yanlış gitti\n{str(e)}", quote=True)
				clearVars()
				cleanFiles()
				return
		else:
			try:
				indiriliyor.reply_document(document=dosyaYolu,disable_notification=True,quote=True,caption=kepsin,thumb="src/file.jpg")
			except FloodWait as f:
				LOGGER.info("Dosya gönderimi / timesleep" + str(f))
				time.sleep(f.x * 1.5)
				indiriliyor.reply_document(document=dosyaYolu,disable_notification=True,quote=True,caption=kepsin,thumb="src/file.jpg")
			except RPCError as e:
				LOGGER.error("RPCError: " + str(e))
			except Exception as e:
				LOGGER.error("Exception:" + str(e))
				message.reply(f"birşeyler yanlış gitti\n{str(e)}", quote=True)
				clearVars()
				cleanFiles()
				return
		toplamGonderilen = toplamGonderilen + os.path.getsize(dosyaYolu)
		try: os.remove(dosyaYolu)
		except Exception as v: LOGGER.error(str(v))
	texto = f"{info}🇹🇷 yükleme bitti 🇬🇧 done uploading.\n" + \
		f"🇹🇷 toplam inen 🇬🇧 total down: {humanbytes(int(indirilenBoyut))}\n" + \
		f"🇹🇷 indirme süresi 🇬🇧 download time: {ReadableTime(indirmeBitti-indirmeBasladi)}\n" + \
		f"🇹🇷 yükleme süresi 🇬🇧 upload time: {ReadableTime(time.time() - c_time)}\n" + \
		f"🇹🇷 toplam süre 🇬🇧 total time: {ReadableTime(time.time() - indirmeBasladi)}\n" + \
		f"{message.from_user.mention()}"
	indiriliyor.reply_text(texto, quote=True)
	indiriliyor.edit_text(texto)
	clearVars()
	cleanFiles()
