import os
import sys

import testcase_base
from bantorra.util.log import LOG as L

class TestCase_Picture(testcase_base.TestCase_Base):

    def picture_crop(self, pic, box="", filename=""):
        try:
            return self.picture.crop_picture(pic, box, filename)
        except Exception as e:
            L.warning(e)

    def picture_find_pattern(self, reference, target):
        try:
            return self.picture.find_pattern(reference, target)
        except Exception as e:
            L.warning(e)

    def picture_is_pattern(self, reference, target):
        try:
            return self.picture.is_pattern(reference, target)
        except Exception as e:
            L.warning(e)

    def ret_rgb(self, pic, box=""):
        try:
            return self.picture.get_rgb(pic, box)
        except Exception as e:
            L.warning(e)
