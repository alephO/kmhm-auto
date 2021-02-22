# This file handles the main loop logic in the console mode.
# Kmhm singleton is handled by this file
from kmhm_singleton import KmhmAuto
from utils.logger import log_adapter


logger = log_adapter.getlogger(__name__)


def main(simple_mode=False):
    kmhm_auto = KmhmAuto()
    loop_flag = True
    while loop_flag:
        logger.debug('Continue admin loop')
        try:
            # startup methods
            kmhm_auto.start_bot()
            if simple_mode:
                while kmhm_auto.simple_continue_loop:
                    kmhm_auto.simple_next_step()
            else:
                while kmhm_auto.continue_loop:
                    kmhm_auto.next_step()
        except Exception as e:
            raise e

        #kmhm_auto.pcdta().chrome_screenshot('1110.png')

        # # TODO: For experiment only. Remove in the end
        # from utils.testing import test_loop
        # test_loop()

        break