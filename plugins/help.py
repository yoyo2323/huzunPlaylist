# HuzunluArtemis - 2021 (Licensed under GPL-v3)

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from pyrogram.types.messages_and_media.message import Message
from HelperFunc.authUserCheck import AuthUserCheck
from HelperFunc.forceSubscribe import ForceSub
from HelperFunc.messageFunc import sendMessage
from HelperFunc.progressMulti import humanbytes
from config import Config
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@Client.on_message(filters.command(Config.HELP_COMMANDS))
async def help(client, message: Message):
	if not await AuthUserCheck(message): return
	if await ForceSub(client, message) == 400: return
	sampleText = ""
	sampleText += f"🇬🇧 You can download a playlist with: /{Config.MUSIC_COMMAND[0]} -Link-\n"
	sampleText += f"Example: `/{Config.MUSIC_COMMAND[0]} https://www.youtube.com/playlist?list=PL9kxHCTcPAEUQrfF0L4TGZkI3hUF3awgD`\n"
	sampleText += "You can reply to message that contains playlist url.\n"
	if Config.SIZE_LIMIT != 0: sampleText += f"Size limit: {humanbytes(Config.SIZE_LIMIT)}"
	if Config.VIDEO_LIMIT != 0:
		if Config.SIZE_LIMIT != 0: sampleText += ", "
		sampleText += f"Video limit: {str(Config.VIDEO_LIMIT)}\n"
	sampleText += f"\n🇹🇷 Bir oynatma listesini şöyle indirebilirsin: /{Config.MUSIC_COMMAND[0]} -Link-\n"
	sampleText += f"Örnek: `/{Config.MUSIC_COMMAND[0]} https://www.youtube.com/playlist?list=PL9kxHCTcPAEUQrfF0L4TGZkI3hUF3awgD`\n"
	sampleText += "Oynatma listesi linki içeren bir mesaj yanıtlarsan da olur.\n"
	if Config.SIZE_LIMIT != 0: sampleText += f"Boyut limiti: {humanbytes(Config.SIZE_LIMIT)}"
	if Config.VIDEO_LIMIT != 0:
		if Config.SIZE_LIMIT != 0: sampleText += ", "
		sampleText += f"Video limiti: {str(Config.VIDEO_LIMIT)}"
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
	await sendMessage(message,toSendStr,reply_markup)
