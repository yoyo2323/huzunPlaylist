# HuzunluArtemis - 2021 (Licensed under GPL-v3)

from pyrogram import Client, filters
from HelperFunc.forceSubscribe import ForceSubSync
from HelperFunc.messageFunc import editMessage, sendMessage
from config import Config
from pyrogram.types.messages_and_media.message import Message
import logging
import time
from HelperFunc.authUserCheck import AuthUserCheck, AuthUserCheckSync
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

@Client.on_message(filters.command(Config.PING_COMMAND))
def ping(client: Client, message: Message):
    if not AuthUserCheckSync(message): return
    if ForceSubSync(client, message) == 400: return
    start_time = int(round(time.time() * 1000))
    reply = sendMessage(message,"Ping")
    end_time = int(round(time.time() * 1000))
    editMessage(reply,f"Pong\n{end_time - start_time} ms")
