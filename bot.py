# HuzunluArtemis - 2021 (Licensed under GPL-v3)

import logging
from config import Config
import pyrogram
import logging, os
from HelperFunc.clean import cleanFiles
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

if __name__ == '__main__':
    
    plugins = dict(root = 'plugins')
    
    app = pyrogram.Client("PlaylistAudioBot",
      workers=343,
      bot_token = Config.BOT_TOKEN,
      api_id = Config.APP_ID,
      api_hash = Config.API_HASH,
      plugins = plugins)
    if os.path.exists('calisiyor.txt'): os.remove("calisiyor.txt")
    app.start()
    

    LOGGER.info(msg="App Started.")
    if Config.OWNER_ID != 0:
      try:
        app.send_message(text= "ayaktayım efendim.\ni am awaken.",chat_id=Config.OWNER_ID)
      except Exception as t:
        LOGGER.error(str(t))
    
    pyrogram.idle()
    
    LOGGER.info(msg="App Stopped.")
    app.stop()
    cleanFiles(exiting=True)
    exit()
    
