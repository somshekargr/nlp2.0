from configparser import ConfigParser
import logging
import logging.handlers as handlers
import os
import sys
config_file_path = './config.ini'
config = ConfigParser()
config.read(config_file_path)
LOG_PATH = config.get("logging","log_path")
LOG_FILE = config.get("logging", "log_file_name")
WHEN = config.get("logging", "when")
BACKUPCOUNT = config.get("logging", "backupcount")

if os.path.exists(LOG_PATH) is False:
    os.mkdir(LOG_PATH)
   
logger = logging.getLogger()
logger.setLevel(logging.INFO)
FORMATTER = logging.Formatter(
    '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', )

# Here we define our formatter
# formatter = logging.Formatter(FORMATTER)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.ERROR)
logHandler = handlers.TimedRotatingFileHandler(LOG_PATH+LOG_FILE , when=WHEN, backupCount=BACKUPCOUNT)
logHandler.setFormatter(FORMATTER)

logger.addHandler(logHandler)
