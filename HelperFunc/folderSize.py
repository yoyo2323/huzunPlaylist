# HuzunluArtemis - 2021 (Licensed under GPL-v3)

import os
import time
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def get_size(start_path = '.'):
    start_time = int(round(time.time() * 1000))
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    end_time = int(round(time.time() * 1000))
    return total_size

def getFolderSize(folder):
    start_time = int(round(time.time() * 1000))
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            if not os.path.islink(itempath):
                total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    end_time = int(round(time.time() * 1000))
    return total_size

