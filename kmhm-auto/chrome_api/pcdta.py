# PCDTA - PyChromeDevTool API handler
import base64

import PyChromeDevTools
import cv2
import numpy
from pyvisauto import Region, FindFailed, ImageMatch
from utils.logger import log_adapter

from constants import VISUAL_URL

logger = log_adapter.getlogger(__name__)


class PCDTA(object):
    def __init__(self):
        self.visual_hook = None
        self.api_hook = None

    def hook_chrome(self, host="localhost", port=9222):
        logger.info('Hooking into chrome')
        self.visual_hook = PyChromeDevTools.ChromeInterface(
            host=host, port=port)
        self.api_hook = PyChromeDevTools.ChromeInterface(host=host, port=port)

        visual_tab = None
        visual_tab_id = None
        api_tab = None
        api_tab_id = None
        for n, tab in enumerate(self.visual_hook.tabs):
            if tab['url'] == VISUAL_URL:
                visual_tab = n
                visual_tab_id = tab['id']

        if visual_tab_id is None:
            logger.error(
                "No Kantai Collection tab found in Chrome. Shutting down "
                "kcauto.")
            raise Exception(
                "No running Kantai Collection tab found in Chrome.")

        self.visual_hook.connect_targetID(visual_tab_id)
        logger.debug(
            f"Connected to visual tab ({visual_tab}:{visual_tab_id})")
        self.visual_hook.Page.enable()

        logger.info('Successfully hook into chrome')

    def start_bot(self):
        """Method that attempts to start Kancolle from the game's splash
        screen. If starting from the splash screen, kcauto will load the data
        from the get_data api call. Otherwise, it will load the stored data
        from previous startups.
        """
        screen = Region()
        # if self.click_existing(screen, 'global|game_start.png'):
        #     Log.log_msg("Starting kancolle from splash screen.")
        #     api.api.update_from_api({
        #         KCSAPIEnum.GET_DATA, KCSAPIEnum.REQUIRE_INFO, KCSAPIEnum.PORT})
        #     self.wait(screen, 'nav|home_menu_sortie.png', 60)
        #     Log.log_success("Kancolle successfully started.")
        #     shp.ships.load_wctf_names(force_update=True)
        # else:
        #     api.api.update_ship_library_from_json()
        # self.sleep()
        return True

    def _get_region(self, region):
        """Helper method that returns a Region based on the region passed in.
        If a Region or Match object is passed in, it will return that  object
        as-is. If a string is passed in, it will look up that string key from
        the pre-defined region dictionary and return it if there is a match.

        Args:
            region (Region, Match str): Region/Match object or string key of
                pre-defined region.

        Raises:
            TypeError: string region key was not found in pre-defined region
                list.

        Returns:
            Region/ImageMatch: Region or ImageMatch object.
        """
        if type(region) == str:
            return self.r[region]
        elif isinstance(region, ImageMatch):
            return region
        else:
            raise TypeError("Invalid region specified.")

    def chrome_screenshot( self, savename=None ):
        self.visual_hook.Page.bringToFront()
        capture1 = self.visual_hook.Page.captureScreenshot()
        if not capture1:
            logger.error( 'Failed to screenshot' )
        c1_bytes = base64.b64decode(capture1['result']['data'])
        c1_arr = numpy.frombuffer(c1_bytes, dtype=numpy.uint8)
        c1_final = cv2.imdecode(c1_arr, flags=cv2.IMREAD_COLOR)
        if savename:
            cv2.imwrite('captured/%s' % savename, c1_final)
        return c1_final

    def test(self):
        pass


pcdta = PCDTA()
