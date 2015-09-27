import sys
import os
import time
import numpy
import cv2
import cv2.cv as cv
from PIL import Image

LIB_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not LIB_PATH in sys.path:
    sys.path.insert(0, LIB_PATH)

from picture import utility
from picture.utility import POINT
from picture.utility import APP_TMP
from picture.utility import LOG as L

THRESHOLD = 0.96

class IO(object):
    def __init__(self):
        pass

    @classmethod
    def get_picture(cls, path):
        try:
            return Image.open(path, 'r')
        except IOError, (errno, strerror):
            L.debug("I/O error(%s): %s" % (errno, strerror))
            raise IOError(strerror)

    @classmethod
    def get_rgb(cls, pic, box=""):
        if box == "":
            box = (0, 0, pic.width, pic.height)
        rgbimg = pic.crop(box).convert("RGB")
        rgb = numpy.array(rgbimg.getdata())
        return [cls.__round(rgb[:,0]),
                cls.__round(rgb[:,1]),
                cls.__round(rgb[:,2])]

    @classmethod
    def crop(cls, pic, box="", filename=""):
        if box == "":
            box = (0, 0, pic.width, pic.height)
        image = pic.crop(box)
        return image.save(filename)

    @classmethod
    def __round(cls, array):
        return int(round(numpy.average(array)))

class PatternMatch(object):

    def __init__(self):
        pass

    @classmethod
    def __patternmatch(cls, reference, target):
        L.debug("reference : %s" % reference)
        img_rgb = cv2.imread(reference)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(target, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        loc = numpy.where( res >= THRESHOLD)
        result = None
        for pt in zip(*loc[::-1]):
            result = POINT(pt[0], pt[1], w, h)
        return result

    @classmethod
    def bool(cls, reference, target):
        result = PatternMatch.__patternmatch(reference, target)
        if result is None:
            return False
        else:
            return True

    @classmethod
    def coordinate(cls, reference, target):
        return PatternMatch.__patternmatch(reference, target)

class Picture(object):
    img = IO()
    pm = PatternMatch()

    def __init__(self):
        pass

    @classmethod
    def get_picture(cls, filename):
        return cls.img.get_picture(filename)

    @classmethod
    def crop_picture(cls, pic, box="", filename=""):
        return cls.img.crop(pic, box, filename)

    @classmethod
    def get_rgb(cls, pic, box=""):
        return cls.img.get_rgb(pic, box)

    @classmethod
    def find_pattern(cls, reference, target):
        return cls.pm.coordinate(reference, target)

    @classmethod
    def is_pattern(cls, reference, target):
        return cls.pm.bool(reference, target)

if __name__ == "__main__":
    pmc = Picture()
    print pmc.find_pattern(os.path.join(APP_TMP, "default_TMP.png"),
                           os.path.join(APP_TMP, "default", "mission.png"))
