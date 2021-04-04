# This is to sample images into file for future study
# Doesn't seems to really needs sqlite for it. Just want to have a try and might be useful
# in the future
from db.sqlite_handler import dbHandler
from utils.img_handler import ImageAdapter, img_handler
from utils.logger import log_adapter

logger = log_adapter.getlogger(__name__)

class ImageSampler:
    def __init__(self, db_handler):
        self.dbh = db_handler
        self.db_tablename = 'img_samples'
        self.db_keyname = 'id'
        db_handler.create_table( self.db_tablename,'%s STRING PRIMARY KEY' % self.db_keyname )

    def log_image(self, img, pp=None):
        # pp is picked pixels in the images
        if isinstance(img, ImageAdapter):
            img = img.arr

        if not pp:
            pp = img_handler.get_picked_pixels(img)

        code = self.pp_to_code(pp)
        logger.debug('Image code is %s' % code)

        if self.dbh.check_exist(self.db_tablename, self.db_keyname, code) == 0:
            filename = "samples/%s.png" % code
            logger.debug("Saving image as %s" % filename)
            img_handler.save_img(filename, img)
            self.dbh.insert( self.db_tablename, "('%s')" % code)

        else:
            logger.debug("Image already in database. Skipping")

    @classmethod
    def pp_to_code(cls, pp):
        s = "rgb"
        for point in pp:
            dt = '{0:03d}{1:03d}{2:03d}'.format(point[0], point[1], point[2])
            s += dt
        return s

image_sampler = ImageSampler( dbHandler )