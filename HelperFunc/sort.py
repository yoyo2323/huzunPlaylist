# HuzunluArtemis - 2021 (Licensed under GPL-v3)
# https://stackoverflow.com/questions/4500564/directory-listing-based-on-time/4500607#4500607

import logging
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def sortMostRecentContentModification(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))

def sortMostRecentMetadataChange(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_ctime
    return list(sorted(os.listdir(path), key=mtime))
