# This file handles the singleton of the main bot logic
from constants import TMP_DICT
from chrome_api.pcdta import pcdta
from enum import Enum

from utils.logger import log_adapter
from utils.img_handler import img_handler
import time


class KmhmAuto(object):
    def __init__(self):
        self._pcdta = pcdta
        self._sm = Kmhm_Sm()
        self._pcdta.hook_chrome(port=TMP_DICT['chrome_debug_port'])
        self._logger = log_adapter.getlogger(__name__)
        self.continue_loop = True
        self.simple_continue_loop = True
        # Screenshot data
        self.sc_data = None

    def start_bot(self):
        self._pcdta.start_bot()

    def next_step(self):
        self.update_sm_if_required()
        if not self._sm.location_valid():
            self._logger.error('Location is Invalid')
            self.continue_loop = False
            return

    def simple_next_step(self):
        self._logger.debug('Simple step')
        sc = img_handler.take_screenshot()
        if sc is not None and not img_handler.img_rough_equal(sc, self.sc_data):
            filename = "maint/" +log_adapter.datetime_str(extention='png')
            self.sc_data = sc
            img_handler.save_img(filename, self.sc_data)
        time.sleep(5)

    def update_sm_if_required(self):
        pass

    def pcdta(self):
        return self._pcdta

class Location(Enum):
    UNDEFINED = 0
    UNSTARTED = 1

class ButtonType(Enum):
    START_GAME = 0

class Kmhm_Sm:
    # State machine of the state
    def __init__(self):
        self._location = Location.UNDEFINED
        self._critical_button = None
        self._critical_button_loc = None

    def location(self):
        return self._location

    def location_valid(self):
        return self._location != Location.UNDEFINED
