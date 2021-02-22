from chrome_api.pcdta import pcdta
from utils.logger import log_adapter
import base64
import numpy
import cv2
import random

logger = log_adapter.getlogger(__name__)


class ImageHandler():
    def __init__(self):
        self.assets = 'assets'

    def take_screenshot(self, writetofile=False, filename=None):
        logger.debug("Taking screenshot")
        pcdta.visual_hook.Page.bringToFront()
        capture1 = pcdta.visual_hook.Page.captureScreenshot()
        if not capture1:
            logger.error('Failed to screenshot')
            return None
        else:
            if isinstance(capture1,tuple):
                capture1 = capture1[0]
            c1_bytes = base64.b64decode(capture1['result']['data'])
            c1_arr = numpy.frombuffer(c1_bytes, dtype=numpy.uint8)
            c1_final = cv2.imdecode(c1_arr, flags=cv2.IMREAD_COLOR)

            if writetofile:
                cv2.imwrite('captured/%s' % filename, c1_final)

            return c1_final

    def save_img(self, filename, img):
        cv2.imwrite('captured/%s' % filename, img)

    @classmethod
    def img_rough_equal(cls, img1, img2):
        if img1 is None or img2 is None:
            if img1 is None and img2 is None:
                return True
            return False

        shape = img1.shape
        if shape != img2.shape:
            return False

        for _ in range(5):
            x = random.randrange(shape[0])
            y = random.randrange(shape[1])
            for i in range(3):
                if img1[x, y, i] != img2[x, y, i]:
                    return False

        return True

    @classmethod
    def find(cls, sc, image, similarity=0.9):
        template = cv2.imread('assets/{}.png'.format(image), cv2.IMREAD_COLOR)
        match = cv2.matchTemplate(sc, template, cv2.TM_CCOEFF_NORMED)

        height, width = template.shape[:2]
        value, location = cv2.minMaxLoc(match)[1], cv2.minMaxLoc(match)[3]
        if value >= similarity:
            return location[0], location[1], width, height
        return None

img_handler = ImageHandler()
