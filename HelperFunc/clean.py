# HuzunluArtemis - 2021 (Licensed under GPL-v3)

import logging
import os, shutil

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def cleanFiles(exiting = False):
    calisiyorYolu = "calisiyor.txt"

    LOGGER.info("files cleared.")
    if exiting:
        try:
            files = ["PlaylistBot.session", "PlaylistBot.session"]
            for it in files:
                if os.path.isfile(it): os.remove(it)
        except Exception as r:
            LOGGER.error("error when delete: "+ str(r))
    try:
        files = [calisiyorYolu]
        for it in files:
            if os.path.isfile(it): os.remove(it)
    except:
        pass
    try:
        shutil.rmtree("musics") # delete folder for user
        os.rmdir("musics")
    except:
        pass
    