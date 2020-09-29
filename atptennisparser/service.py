from app import update_db

# simple linux service to backup redis cache

from datetime import datetime
import os
import glob
import time
import shutil
from datetime import datetime
from config import Config

import logging
from logging.handlers import RotatingFileHandler

def backup_redis_task():
    logger.info("running backup redis task at {}".format(datetime.now()))

    ret_code = os.system("docker exec pastebin-redis redis-cli -a {} --rdb /data/dump.rdb".format(
        os.environ['REDIS_PASS']))
    if ret_code == 0:
        logger.info("backup successful")
    else:
        logger.info("unable to backup data")

# create logger
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

# create file handler and set level to debug
fh = RotatingFileHandler(Config.SERVICE_LOG_FILE, maxBytes=2000, backupCount=1)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

while True: # run task forever

    try: # update_db
        logger.info("Running update_db at {}".format(datetime.now()))
        update_db()
        logger.info("Update finished")
    except: # retry again later
        logger.info("Unable to update_db (Exception occured)")

    # run every hour
    time.sleep(60 * 60)
