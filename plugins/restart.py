# HuzunluArtemis - 2021 (Licensed under GPL-v3)

from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message
from HelperFunc.clean import cleanFiles
from HelperFunc.messageFunc import sendMessage
from HelperFunc.ytdl import clearVars
from HelperFunc.updatePackage import updateRequirements
from config import Config
import logging, heroku3
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@Client.on_message(filters.command(Config.RESTART_COMMAND))
def restart(client, message: Message):
    if not (Config.OWNER_ID != 0 and message.from_user.id == Config.OWNER_ID): return
    cmd = message.text.split(' ', 1)
    dynoRestart = False
    dynoKill = False
    if len(cmd) == 2:
        dynoRestart = (cmd[1].lower()).startswith('d')
        dynoKill = (cmd[1].lower()).startswith('k')
    if (not Config.HEROKU_API_KEY) or (not Config.HEROKU_APP_NAME):
        LOGGER.info("If you want Heroku features, fill Config.HEROKU_APP_NAME Config.HEROKU_API_KEY vars.")
        dynoRestart = False
        dynoKill = False
    if dynoRestart:
        LOGGER.info("Dyno Restarting.")
        message.reply_text('Dyno Restarting.')
        heroku_conn = heroku3.from_key(Config.HEROKU_API_KEY)
        app = heroku_conn.app(Config.HEROKU_APP_NAME)
        app.restart()
    elif dynoKill:
        LOGGER.info("Killing Dyno. MUHAHAHA")
        message.reply_text('Killing Dyno')
        heroku_conn = heroku3.from_key(Config.HEROKU_API_KEY)
        app = heroku_conn.app(Config.HEROKU_APP_NAME)
        proclist = app.process_formation()
        for po in proclist: app.process_formation()[po.type].scale(0)
    else:
        toSendStr = "🇹🇷 Yeniden Başlatıldı"
        toSendStr += "\n🇬🇧 Restarted"
        updateRequirements('requirements.txt')
        clearVars()
        cleanFiles()
        sendMessage(message, toSendStr)
