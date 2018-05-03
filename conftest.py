import sys
import logging
import pathlib


sys.path.insert(0, str(pathlib.Path('.').resolve() / 'src'))


from utils import logger # noqa


logger.set_level(logging.FATAL, 'http')
# logger.set_level(LOG_LEVEL_METRIC, 'consensus')
logging.getLogger('urllib3').setLevel(logging.FATAL)
