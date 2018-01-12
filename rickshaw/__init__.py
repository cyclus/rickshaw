import logging
import os

from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
log_handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(fmt='%(message)s %(asctime)s %(created)f '
                                         '%(pathname)s %(funcName)s %(levelname)s '
                                         '%(lineno)d %(process)d %(processName)s')
file_handler = logging.FileHandler('log-rickshaw.json')
file_handler.setFormatter(formatter)
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)
logger.addHandler(file_handler)

__version__ = '1.5.3'
