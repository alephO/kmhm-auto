import logging
import sys
from datetime import datetime

from constants import TMP_DICT


class LogAdapter(object):
    def getlogger(self, module_name):
        logger = logging.getLogger(module_name)

        # TODO: This need to be from config
        logger.setLevel(TMP_DICT['log_level'])

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    @classmethod
    def datetime_str(self, format=None, extention=None):
        now = datetime.now()
        if not format:
            format = "%Y%m%d-%H%M%S"
        dt_string = now.strftime(format)
        if extention:
            dt_string += '.' + extention
        return dt_string


log_adapter = LogAdapter()
