# HuzunluArtemis - 2021 (Licensed under GPL-v3)

from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message
from pyrogram.errors import RPCError
import logging, os, time, re
from HelperFunc.authUserCheck import AuthUserCheckSync
from HelperFunc.clean import cleanFiles
from natsort import natsorted
from HelperFunc.forceSubscribe import ForceSubSync
from HelperFunc.messageFunc import editMessage, sendAudio, sendMessage
from HelperFunc.progressMulti import ReadableTime, humanbytes
from HelperFunc.ytdl import clearVars, getVideoDetails, ytdDownload
from config import Config
from HelperFunc.folderSize import get_size
from HelperFunc.updatePackage import updatePipPackage
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

outDir = "musics"
quee = []

@Client.on_message(filters.command(Config.MUSIC_COMMAND))
def playlist(client, message: Message):
	if not AuthUserCheckSync(message): return
	if ForceSubSync(client, message) == 400: return
	if not os.path.exists(outDir): os.makedirs(outDir)
	url = ""
	if not message.reply_to_message:
		url = message.text.split(' ', 1)
		try: url = url[1]
		except IndexError:
			sendMessage(message,"🇬🇧 click and read: /help\n🇹🇷 tıkla ve oku: /yardim")
			return
	else: url = message.reply_to_message.text
	try: url = re.match(r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*", url)[0]
	except TypeError:
		sendMessage(message,"🇬🇧 click and read: /help\n🇹🇷 tıkla ve oku: /yardim")
		return

	# her kullanıcı aynı anda 1 sıra
	islemLim = 0
	if not message.from_user.id in Config.PREMIUM_USERS: islemLim = Config.PROCESS_PER_USER_FREE_USER
	else: islemLim = Config.PROCESS_PER_USER_PREMIUM_USER
	if islemLim != 0:
		suankiIslem = 1
		for sira in quee:
			if sira[0].from_user.id == message.from_user.id: suankiIslem = suankiIslem + 1
		if suankiIslem > islemLim:
			sendMessage(message,f"🇬🇧 {str(islemLim)} process in same time per user\n" + \
				f"If you want to be premium user, contact: @{Config.CHANNEL_OR_CONTACT}" + \
				f"\n\n🇹🇷 Her kullanıcı anlık {str(islemLim)} işlem yapabilir.\n" + \
				f"Premium olmak istiyorsanız iletişim: @{Config.CHANNEL_OR_CONTACT}")
			return
	# her kullanıcı aynı anda 1 sıra

	ret = sendMessage(message, f"🇬🇧 Added to Quee: {len(quee)+1}\nWait your turn" + \
		f"\n\n🇹🇷 Sıraya Eklendi: {len(quee)+1}\nSıranızı bekleyin")
	quee.append([message,ret,url])
	if len(quee) == 1: addTask(gelen=message,duzenlenecek=ret,url=url)

def onTaskComplete():
	clearVars()
	cleanFiles()
	if len(quee) > 0: del quee[0]
	if len(quee) > 0: addTask(quee[0][0],quee[0][1],quee[0][2])
	# kullanım: tüm görevleri bir listeye topla
	# hepsinin ilk değeri mesaj, ikincisi düzenlenecek mesaj, üçüncüsü url.

def addTask(gelen: Message, duzenlenecek:Message, url:str):
	
	VIDEO_SUFFIXES = ("MKV", "MP4", "MOV", "WMV", "3GP", "MPG", "WEBM", "AVI", "FLV", "M4V", "GIF")
	AUDIO_SUFFIXES = ("MP3", "M4A", "M4B", "FLAC", "WAV", "AIF", "OGG", "AAC", "DTS", "MID", "AMR", "MKA")
	IMAGE_SUFFIXES = ("JPG", "JPX", "PNG", "WEBP", "CR2", "TIF", "BMP", "JXR", "PSD", "ICO", "HEIC", "JPEG")

	info = f"Bilgi / Info:\n\n- user: {gelen.from_user.mention()} (`{str(gelen.from_user.id)}`)\n- link: `{url}`"
	info += f'\n- uptime: `{ReadableTime(time.time() - Config.botStartTime)}`\n\n'
	text = info + "🇹🇷 inceleniyor.\nbu işlem her video için 1 saniye demektir.\neğer 60 videonuz varsa, 60 saniye bekleyin.\n\n"
	text += "🇬🇧 i am looking for you.\nthis means 1 second for each video.\nif you have 60 videos, wait 60 seconds.\n"

	updatePipPackage("yt-dlp")
	boyut = None
	try: _, boyut, _, _ = getVideoDetails(url, duzenlenecek)
	except TypeError as e:
		LOGGER.info(str(e))
		onTaskComplete()

	#video limit
	vidLim = 0
	if not gelen.from_user.id in Config.PREMIUM_USERS: vidLim = Config.VIDEO_LIMIT_FREE_USER
	else: vidLim = Config.VIDEO_LIMIT_PREMIUM_USER
	if (vidLim != 0) and (len(boyut) > vidLim):
		try: duzenlenecek.edit_text(f"🇬🇧 video limit: {str(vidLim)} yours: {len(boyut)}\n" + \
			f"If you want to be premium user, contact: @{Config.CHANNEL_OR_CONTACT}" + \
			f"\n\n🇹🇷 video limiti: {str(vidLim)} seninki: {len(boyut)}\n" + \
			f"Premium olmak istiyorsanız iletişim: @{Config.CHANNEL_OR_CONTACT}")
		except Exception as h: LOGGER.info(str(h))
		onTaskComplete()

	# size limit
	sizeLim = 0
	if not gelen.from_user.id in Config.PREMIUM_USERS: sizeLim = Config.SIZE_LIMIT_FREE_USER
	else: sizeLim = Config.SIZE_LIMIT_PREMIUM_USER
	toplamBoyut = 0
	for x in range(len(boyut)): toplamBoyut = toplamBoyut + int(boyut[x])
	if (sizeLim != 0) and (toplamBoyut > sizeLim):
		try: duzenlenecek.edit_text(f"🇬🇧 Size limit: {str(humanbytes(sizeLim))} yours: {humanbytes(toplamBoyut)}\n" + \
			f"If you want to be premium user, contact: @{Config.CHANNEL_OR_CONTACT}" + \
			f"\n\n🇹🇷 Boyut limiti: {str(humanbytes(sizeLim))} seninki: {humanbytes(toplamBoyut)}\n" + \
			f"Premium olmak istiyorsanız iletişim: @{Config.CHANNEL_OR_CONTACT}")
		except Exception as h: LOGGER.info(str(h))
		onTaskComplete()
	
	try: duzenlenecek.edit_text(f"{info}🇹🇷 indirilecek 🇬🇧 will down: {humanbytes(int(toplamBoyut))}")
	except: pass
	indirmeBasladi = time.time()
	ytdDownload(url, duzenlenecek, info)
	indirmeBitti = time.time()
	LOGGER.info(url)
	toup = os.listdir(outDir)
	for filo in toup:
		if filo.upper().endswith(IMAGE_SUFFIXES) or filo.upper().endswith(VIDEO_SUFFIXES): os.remove(os.path.join(outDir, filo))
	toup = natsorted(os.listdir(outDir))
	
	LOGGER.info("#toup: " + ", ".join(toup))
	toplamarsiv = str(len(toup))
	indirilenBoyut = get_size(outDir)
	editMessage(duzenlenecek,f"{info}🇹🇷 toplam inen 🇬🇧 total down: {humanbytes(int(indirilenBoyut))}")
	
	c_time = time.time()
	suan = 0
	toplamGonderilen = 0
	for filo in toup:
		suan = suan + 1
		kepsin = f'<a href="{Config.FLAME_URL}">🔥</a> {filo}\n`{url}`'
		if int(toplamarsiv) != 1: kepsin += f'\n`{suan}.{toplamarsiv}`'
		dosyaYolu = os.path.join(outDir, filo)
		dosyaBoyutu = os.path.getsize(dosyaYolu)
		if dosyaBoyutu > Config.TG_SPLIT_SIZE:
			sendMessage(gelen,f"büyük dosya\ntg size limit:\n\n{filo}")
			continue
		if filo.upper().endswith(AUDIO_SUFFIXES):
			try:
				prog = f"{info}Dosyalar / Files:\n\n- mesaj: {duzenlenecek.link}\n" + \
				f"- anlık sıra / file quee: {str(suan)}/{toplamarsiv}\n" + \
				f"- yüklenen / uploading:\n`{filo}`"
				sendAudio(duzenlenecek,dosyaYolu,kepsin,prog,duzenlenecek,c_time,indirilenBoyut,toplamGonderilen)
				if int(toplamarsiv) != 1: time.sleep(Config.SLEEP_BETWEEN_SEND_FILES)
			except RPCError as e:
				LOGGER.error("RPCError: " + str(e))
			except Exception as e:
				LOGGER.error("Exception:" + str(e))
				onTaskComplete()
		toplamGonderilen = toplamGonderilen + dosyaBoyutu
	texto = f"{info}🇹🇷 yükleme bitti 🇬🇧 done uploading.\n" + \
		f"🇹🇷 toplam inen 🇬🇧 total down: {humanbytes(int(indirilenBoyut))}\n" + \
		f"🇹🇷 indirme süresi 🇬🇧 download time: {ReadableTime(indirmeBitti-indirmeBasladi)}\n" + \
		f"🇹🇷 yükleme süresi 🇬🇧 upload time: {ReadableTime(time.time() - c_time)}\n" + \
		f"🇹🇷 toplam süre 🇬🇧 total time: {ReadableTime(time.time() - indirmeBasladi)}\n" + \
		f"🇹🇷 toplam dosya 🇬🇧 total file: {toplamarsiv}\n" + \
		f'<a href="{duzenlenecek.link}">🇹🇷 indirici mesaj 🇬🇧 downloader</a>'
	sendMessage(duzenlenecek,texto)
	editMessage(duzenlenecek,texto)
	onTaskComplete()
