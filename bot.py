# HuzunluArtemis - 2021 (Licensed under GPL-v3)

from HelperFunc.progressMulti import ReadableTime
from config import Config
import logging, time
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from HelperFunc.clean import cleanFiles
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class Bot(Client):

    def __init__(self):
        super().__init__(
            session_name=Config.SESSION,
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=343,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username = '@' + me.username
        LOGGER.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        if Config.OWNER_ID != 0:
            try:
                await self.send_message(text= "🇬🇧 i reborn from the ashes of darkness\n🇹🇷 karanlığın küllerinden yeniden doğdum",
                    chat_id=Config.OWNER_ID)
            except Exception as t:
                LOGGER.error(str(t))

    async def stop(self, *args):
        if Config.OWNER_ID != 0:
            texto = f"🇬🇧 I took my last breath.\nthe age i died: {ReadableTime(time.time() - Config.botStartTime)}" + \
                    f"\n\n🇹🇷 son nefesimi verdim.\nöldüğümde yaşım: {ReadableTime(time.time() - Config.botStartTime)}"
            try:
                if Config.SEND_LOGS_WHEN_DYING:
                    await self.send_document(document='log.txt',caption=texto, chat_id=Config.OWNER_ID, thumb='src/file.jpg')
                else:
                    await self.send_message(text= texto,chat_id=Config.OWNER_ID)
            except Exception as t:
                LOGGER.warning(str(t))
        await super().stop()
        cleanFiles(exiting=True)
        LOGGER.info(msg="App Stopped.")
        exit()

app = Bot()
app.run()
