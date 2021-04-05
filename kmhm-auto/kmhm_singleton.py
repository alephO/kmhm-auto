# This file handles the singleton of the main bot logic
from constants import TMP_DICT
from chrome_api.pcdta import pcdta
from enum import Enum

from utils.logger import log_adapter
from utils.img_handler import img_handler
from db.sqlite_handler import dbHandler
from db.image_samples import image_sampler
import time
import random


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
        # Simple step list and corresponding templates
        self.sp_lst = [
            'events',
            'e_ssshz/title',
            'e_ssshz/stages',
            'e_ssshz/e1',
            ['menu/light','menu/hsxg'],
            'menu/hsxg',
            'e_ssshz/gotostage',
            'e_ssshz/callfor',
            'e_ssshz/attack',
            ['popup/discover', 'popup/ok'],
            'menu/nextstep',
            #['popup/ap1', 'popup/apto3', 'popup/addap'],
            'popup/addap',
            'menu/redo'
        ]

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
        sc = img_handler.take_screenshot(trim=True)
        non_changed = 0
        # sc is an Image adapter. Can't use if sc
        if sc is not None:
            old_sc_pp = img_handler.get_picked_pixels(self.sc_data)
            sc_pp = img_handler.get_picked_pixels(sc)
            if not img_handler.pixels_rough_equal(old_sc_pp, sc_pp):
                self.sc_data = sc
                # filename = "maint/" +log_adapter.datetime_str(extention='png')
                filename = "maint/current.png"
                self._logger.debug("Saving image as %s" % filename)
                img_handler.save_img(filename, self.sc_data)
                image_sampler.log_image(sc, sc_pp)
            else:
                self._logger.debug("Don't save image. Didn't change a lot")
                self.sc_data = sc

            if not img_handler.pixels_rough_equal(old_sc_pp, sc_pp, rate=0.99) or \
                    non_changed > 5:
                # Must 100% match to skip match process
                non_changed = 0
                simple_clicked = self.simple_check_and_click()
            else:
                non_changed += 1
        sleep_time = random.randint(1000, 2000) / 1000
        time.sleep(sleep_time)

    def simple_check_and_click(self):
        clicked = False
        def _click_name( name ):
            m = img_handler.find(self.sc_data, name)
            if m:
                self._logger.debug("Found %s. Location is %i-%i, size is %i-%i, sc-offset is %i-%i"
                                   % (name, m[0], m[1], m[2], m[3],
                                      self.sc_data.x_delta, self.sc_data.y_delta))
                loc_x, loc_y, size_x, size_y = m
                rand_x = random.randrange(2, size_x - 1)
                rand_y = random.randrange(2, size_y - 1)
                sum_x = self.sc_data.x_delta + loc_x + rand_x
                sum_y = self.sc_data.y_delta + loc_y + rand_y

                self._logger.debug("Try to click %i-%i" % (sum_x, sum_y))
                self._pcdta.click(sum_x, sum_y)
                return True
            return False

        for act in self.sp_lst:
            if isinstance(act, list):
                if not act:
                    continue
                m = img_handler.find(self.sc_data, act[0])
                if not m:
                    continue
                self._logger.debug("Entering unit action " + act[0])
                for it in act:
                    while not _click_name(it):
                        time.sleep(2)

                clicked = True
                break
            if _click_name( act ):
                clicked = True
                break
        return clicked

    def update_sm_if_required(self):
        pass

    def pcdta(self):
        return self._pcdta

    def cleanup(self):
        self._logger.debug("Running singleton's cleanup function")
        dbHandler.cleanup()


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
