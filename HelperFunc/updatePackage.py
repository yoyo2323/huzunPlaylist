# HuzunluArtemis - 2021 (Licensed under GPL-v3)

import subprocess
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def updateRequirements(ilename:str):
    with open(ilename) as f: reqs = f.readlines()
    for req in reqs: updatePipPackage(req)

def updatePipPackage(packName:str):
    if (not packName) or (packName == "") or (packName == " "):
        LOGGER.error("packname was null")
        return
    UPDATE_COMMAND = f"pip install {packName} -U"
    try:
        process = subprocess.Popen(UPDATE_COMMAND,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,shell=True)
        stdout, stderr = process.communicate()
        tore = ""
        torebool = False
        stderr = stderr.decode()
        stdout = stdout.decode()
        if stdout:
            tore = tore + stdout
            torebool = True
        if stderr:
            tore = tore + stderr
            torebool = False
        LOGGER.info(tore)
        return tore, torebool
    except Exception as u:
        LOGGER.error("updater hata: " + str(u))
