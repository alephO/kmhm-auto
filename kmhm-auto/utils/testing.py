import pyautogui
from pyvisauto import Region

from chrome_api.pcdta import pcdta
from utils.logger import log_adapter
import base64
import numpy
import cv2

logger = log_adapter.getlogger(__name__)


def test_loop():
    logger.debug('Screenshoting whole screen')
    # region = Region()
    # capture = pyautogui.screenshot('captured/loop.png', region=(region.x, region.y, region.w, region.h))

    pcdta.visual_hook.Page.bringToFront()
    capture1 = pcdta.visual_hook.Page.captureScreenshot()
    if not capture1:
        logger.error('Failed to screenshot')
    c1_bytes = base64.b64decode(capture1['result']['data'])
    c1_arr = numpy.frombuffer(c1_bytes,dtype=numpy.uint8)
    c1_final = cv2.imdecode(c1_arr, flags=cv2.IMREAD_COLOR)
    cv2.imwrite('captured/loop_ca.png', c1_final)
