# service to parse data from atptour website

from app import update_db

from datetime import datetime
import os
import glob
import time
import shutil
from datetime import datetime
from config import Config

import logging
from logging.handlers import RotatingFileHandler

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
fh = RotatingFileHandler(Config.SERVICE_LOG, maxBytes=2000, backupCount=1)
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
