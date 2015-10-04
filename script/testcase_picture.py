import os
import sys

import testcase_base
from bantorra.util.log import LOG as L

class TestCase_Picture(testcase_base.TestCase_Base):

    @classmethod
    def picture_crop(cls, pic, box="", filename=""):
        try:
            return cls.picture.crop_picture(pic, box, filename)
        except Exception as e:
            L.warning(e)

    @classmethod
    def picture_find_pattern(cls, reference, target):
        try:
            return cls.picture.find_pattern(reference, target)
        except Exception as e:
            L.warning(e)

    @classmethod
    def picture_is_pattern(cls, reference, target):
        try:
            return cls.picture.is_pattern(reference, target)
        except Exception as e:
            L.warning(e)

    @classmethod
    def ret_rgb(cls, pic, box=""):
        try:
            return cls.picture.get_rgb(pic, box)
        except Exception as e:
            L.warning(e)
