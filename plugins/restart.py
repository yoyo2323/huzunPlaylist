# HuzunluArtemis - 2021 (Licensed under GPL-v3)

from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message
from HelperFunc.clean import cleanFiles
from HelperFunc.messageFunc import sendMessage
from HelperFunc.ytdl import clearVars
from HelperFunc.updatePackage import updateRequirements
from config import Config
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@Client.on_message(filters.command(Config.RESTART_COMMAND))
def restart(client, message: Message):
    if not (Config.OWNER_ID != 0 and message.from_user.id == Config.OWNER_ID): return
    toSendStr = "🇹🇷 Yeniden Başlatıldı"
    toSendStr += "\n🇬🇧 Restarted"
    updateRequirements('requirements.txt')
    clearVars()
    cleanFiles()
    sendMessage(message,toSendStr)
