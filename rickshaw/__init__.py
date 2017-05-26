import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logging.basicConfig(filename='myapp.log', level=logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(fmt='%(message)s %(asctime)s %(created)f '
                                         '%(pathname)s %(funcName)s %(levelname)s '
                                         '%(lineno)d %(process)d %(processName)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


__version__ = "0.0.1"
