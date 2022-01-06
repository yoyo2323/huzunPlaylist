# HuzunluArtemis - 2021 (Licensed under GPL-v3)

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from pyrogram.types.messages_and_media.message import Message
from HelperFunc.authUserCheck import AuthUserCheckSync
from HelperFunc.forceSubscribe import ForceSubSync
from HelperFunc.messageFunc import sendMessage
from HelperFunc.progressMulti import humanbytes
from config import Config
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@Client.on_message(filters.command(Config.HELP_COMMANDS))
def help(client, message: Message):
	if not AuthUserCheckSync(message): return
	if ForceSubSync(client, message) == 400: return
	sampleText = ""
	sampleText += f"🇬🇧 You can download a playlist with: /{Config.MUSIC_COMMAND[0]} -Link-\n"
	sampleText += f"Example: `/{Config.MUSIC_COMMAND[0]} https://www.youtube.com/playlist?list=PL9kxHCTcPAEUQrfF0L4TGZkI3hUF3awgD`\n"
	sampleText += "You can reply to message that contains playlist url.\n"
	sampleText += f"\n🇹🇷 Bir oynatma listesini şöyle indirebilirsin: /{Config.MUSIC_COMMAND[0]} -Link-\n"
	sampleText += f"Örnek: `/{Config.MUSIC_COMMAND[0]} https://www.youtube.com/playlist?list=PL9kxHCTcPAEUQrfF0L4TGZkI3hUF3awgD`\n"
	sampleText += "Oynatma listesi linki içeren bir mesaj yanıtlarsan da olur.\n\n"
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
	sampleText += f"🌈 Plan: {plan}\n🔑 Size Limit / Boyut Limiti: {sizeLim}\n" + \
		f"🌿 Quee Limit / Sıra Limiti: {str(QueeLim)}\n🥕 Video Limit / Video Limiti: {str(vidLim)}"
	tumad = message.from_user.first_name
	if message.from_user.last_name != None: tumad += f" {message.from_user.last_name}"
	toSendStr = f"Esenlikler / Hi {tumad}\n\n" + sampleText
	reply_markup = None
	if Config.UPDATES_CHANNEL != None and Config.UPDATES_CHANNEL != "" and Config.UPDATES_CHANNEL != " ":
		reply_markup=InlineKeyboardMarkup(
			[
				[InlineKeyboardButton(
				text = "🔥 Güncellemeler / Updates",
				url = "https://t.me/" + Config.UPDATES_CHANNEL)
				]
			])
	sendMessage(message,toSendStr,reply_markup)
