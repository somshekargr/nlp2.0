import logging
import logging.handlers as handlers
import time

FORMATTER = log_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

logger = logging.getLogger('my_app')
logger.setLevel(logging.INFO)

## Here we define our formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logHandler = handlers.TimedRotatingFileHandler('normal.log', when='M', interval=1, backupCount=0)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(FORMATTER)

# errorLogHandler = handlers.RotatingFileHandler('error.log', maxBytes=5000, backupCount=0)
# errorLogHandler.setLevel(logging.ERROR)
# errorLogHandler.setFormatter(formatter)

logger.addHandler(logHandler)
# logger.addHandler(errorLogHandler)

def main():
    while True:
        time.sleep(1)
        logger.info("A Sample Log Statement")
        logger.error("An error log statement")

main()