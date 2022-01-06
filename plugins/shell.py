# HuzunluArtemis - 2021 (Licensed under GPL-v3)

from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message
from HelperFunc.messageFunc import sendDocument, sendMessage
from config import Config
import subprocess, logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

@Client.on_message(filters.command(Config.SHELL_COMMAND))
def shell(client: Client, message: Message):
    if Config.OWNER_ID == 0: LOGGER.warning("owner id was 0. shell cannot run.")
    if not (Config.OWNER_ID != 0 and message.from_user.id == Config.OWNER_ID): return
    try:
        cmd = message.text.split(' ', 1)
        if len(cmd) == 1:
            sendMessage(message,'🇬🇧 No command to execute was given.\n🇹🇷 Boşluk bırakıp komut gir zırcahil seni.')
            return
        cmd = cmd[1]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        reply = ''
        stderr = stderr.decode()
        stdout = stdout.decode()
        if stdout: reply += f"Stdout:\n`{stdout}`\n"
        if stderr: reply += f"Stderr:\n`{stderr}`\n"
        if len(reply) > 3000:
            with open('shell.txt', 'w') as file: file.write(reply)
            sendDocument(message,'shell.txt')
        else: sendMessage(message,reply)
    except Exception as e:
        LOGGER.error(str(e))
        sendMessage(message,"🇬🇧 Maybe your shell message was empty.\n🇹🇷 Boş bir şeyler döndü valla.")
