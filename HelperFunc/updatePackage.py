# HuzunluArtemis - 2021 (Licensed under GPL-v3)

import subprocess, logging

from config import Config
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def updateRequirements(ilename:str):
    with open(ilename) as f: reqs = f.readlines()
    for req in reqs: updatePipPackage(req)

def updatePipPackage(packName:str):
    UPDATE_COMMAND = f"pip install {packName} -U"
    process = None
    try:
        process = subprocess.Popen(UPDATE_COMMAND,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,shell=True)
    except Exception as u:
        LOGGER.error("arşivlenirken hata: " + str(u))
    stdout, stderr = process.communicate()
    tore = ""
    torebool = False
    stderr = stderr.decode('utf-8')
    stdout = stdout.decode('utf-8')
    if stdout:
        tore = tore + stdout
        torebool = True
    if stderr:
        tore = tore + stderr
        torebool = False
    LOGGER.info(tore)
    return tore, torebool
