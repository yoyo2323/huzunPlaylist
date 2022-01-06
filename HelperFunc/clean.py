# HuzunluArtemis - 2021 (Licensed under GPL-v3)

import os, shutil, logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def cleanFiles(exiting = False):

    LOGGER.info("files cleared.")
    if exiting:
        try:
            files = ["PlaylistAudioBot.session", "PlaylistAudioBot.session"]
            for it in files:
                if os.path.isfile(it): os.remove(it)
        except Exception as r:
            LOGGER.error("error when delete: "+ str(r))
    try:
        shutil.rmtree("musics") # delete folder for user
        os.rmdir("musics")
    except:
        pass
    