from chrome_api.pcdta import pcdta
from utils.logger import log_adapter
import base64
import numpy
import math
import cv2
import random
from constants import TMP_DICT

logger = log_adapter.getlogger(__name__)


class ImageHandler():
    def __init__(self):
        self.assets = 'assets'
        self.game_height = TMP_DICT['game_height']
        # Game height is not at the middle. Add a delta at this time.
        self.game_h_delta = TMP_DICT['game_h_delta']
        self.game_width = TMP_DICT['game_width']

    def take_screenshot(self, trim=False, writetofile=False, filename=None, no_adapter=False ):
        logger.debug("Taking screenshot")
        pcdta.visual_hook.Page.bringToFront()
        capture1 = pcdta.visual_hook.Page.captureScreenshot( captureBeyondViewport=True )
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

            if not no_adapter:
                c1_final = ImageAdapter( c1_final )

            if trim:
                c1_final = self.trim_game_window( c1_final )
            return c1_final

    def save_img(self, filename, img):
        if isinstance(img, ImageAdapter):
            img = img.arr
        cv2.imwrite('captured/%s' % filename, img)

    def trim_game_window( self, img ):
        if isinstance(img, ImageAdapter):
            img_array = img.arr
        else:
            assert isinstance(img, numpy.ndarray)
            img_array = img
        assert isinstance(img_array, numpy.ndarray)
        img_h, img_w, _ = img_array.shape
        if img_h < self.game_height or img_w < self.game_width:
            logger.debug("Image too small to trim. Return as is.")
            return img
        w_start = int( math.floor( ( img_w - self.game_width ) / 2 ) )
        w_end = int(math.ceil((img_w + self.game_width) / 2))
        h_start = int( math.floor( ( img_h - self.game_height ) / 2 ) )
        h_end = int(math.ceil((img_h + self.game_height) / 2))

        h_start += self.game_h_delta
        h_end += self.game_h_delta

        img_array = img_array[h_start:h_end+1, w_start:w_end+1, :]
        if isinstance(img, ImageAdapter):
            img.arr = img_array
            img.x_delta += w_start
            img.y_delta += h_start
            return img
        else:
            return img_array

    @classmethod
    def img_rough_equal(cls, img1, img2):
        if img1 is None or img2 is None:
            if img1 is None and img2 is None:
                return True
            return False

        if isinstance(img1, ImageAdapter):
            img1 = img1.arr

        if isinstance(img2, ImageAdapter):
            img2 = img2.arr

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
        if isinstance(image, ImageAdapter):
            image = image.arr
        template = cv2.imread('assets/{}.png'.format(image), cv2.IMREAD_COLOR)
        match = cv2.matchTemplate(sc, template, cv2.TM_CCOEFF_NORMED)

        height, width = template.shape[:2]
        value, location = cv2.minMaxLoc(match)[1], cv2.minMaxLoc(match)[3]
        if value >= similarity:
            return location[0], location[1], width, height
        return None

class ImageAdapter:
    def __init__(self, arr, x_delta = 0, y_delta = 0):
        self.arr = arr
        self.x_delta = x_delta
        self.y_delta = y_delta

img_handler = ImageHandler()
