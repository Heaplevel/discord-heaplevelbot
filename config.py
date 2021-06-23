import logging

logger = logging.getLogger('bot_logger')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(filename=f"./logs/bot_debug.log",
                         encoding='utf-8', mode='w+')

logger.addHandler(fh)