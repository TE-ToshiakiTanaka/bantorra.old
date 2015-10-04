import os
import sys
import time

import testcase_browser
import testcase_picture

from bantorra.util import define
from bantorra.util.log import LOG as L

class TestCase_Base(testcase_picture.TestCase_Picture,
                    testcase_browser.TestCase_Browser):

    def __init__(self, *args, **kwargs):
        super(TestCase_Base, self).__init__(*args, **kwargs)

    def get_reference(self, reference):
        return os.path.join(define.APP_TMP,
            self.config["player.name"], reference)

    def get_target(self, target):
        return os.path.join(define.APP_TMP, target)

    def browser_login(self):
        self.browser.driver.find_element_by_id(self.get("dmm.login")).send_keys(self.get("args.username"))
        self.browser.driver.find_element_by_id(self.get("dmm.password")).send_keys(self.get("args.password"))
        self.browser.driver.find_element_by_class_name(self.get("dmm.submit")).click()
        time.sleep(1)

    def browser_capture(self, filename=""):
        if filename == "": filename = "capture.png"
        return self.browser_screenshot(filename)

    def enable(self, reference, target=""):
        L.debug("Reference : %s " %reference)
        if target == "":
            target = self.browser_capture(self.get("player.capture"))
        return self.picture_is_pattern(
            self.get_target(target), self.get_reference(reference))

    def enable_timeout(self, reference, target="", loop=5, timeout=5):
        result = False
        for i in xrange(loop):
            if self.enable(reference, target):
                result = True
                break
            time.sleep(timeout)
        return result

    def crop(self, reference, result, filename=""):
        if filename == "":
            filename = self.get_target(self.get("player.capture_tmp"))
        if result == None:
            return self.get_target(reference)
        box = (result.x, result.y, result.width + result.x, result.height + result.y)
        L.debug("Crop Target : %s" % box)
        L.debug("Reference   : %s " % self.get_target(reference))
        self.picture_crop(
            self.pic().get_picture(self.get_target(reference)), box, filename)
        return filename

    def find(self, reference, target=""):
        L.debug("Reference : %s " %reference)
        if target == "":
            target = self.browser_capture(self.get("player.capture"))
        result = self.picture_find_pattern(
            self.get_target(target), self.get_reference(reference))
        if not result == None:
            return result
        else:
            return None

    def enable_timeout_crop_box(self, target, box, filename="", loop=5, timeout=5):
        if filename == "":
            filename = self.get("player.capture")
            self.browser_capture(filename)
        result = self.crop(filename, box)
        if self.enable_timeout(target, result, loop, timeout):
            return True
        else:
            return False

    def enable_timeout_crop(self, reference, target, filename="", loop=5, timeout=5):
        if filename == "":
            filename = self.get("player.capture")
        return self.enable_timeout_crop_box(target, self.find(reference), filename, loop, timeout)

    def tap_coordinate(self, x, y):
        L.debug("Tap Coordinate : (x, y) = (%s, %s)" % (x, y))
        self.browser_click(self.get("dmm.target"), x, y)

    def tap(self, reference, target=""):
        L.debug("Tap Reference : %s " %reference)
        if target == "":
            target = self.browser_capture(self.get("player.capture"))
        result = self.picture_find_pattern(
            self.get_target(target), self.get_reference(reference))
        if not result == None:
            L.debug("Tap : (x, y) = (%s, %s)"
                % (result.x + (result.width / 2), result.y + (result.height / 2)))
            self.tap_coordinate(result.x + (result.width / 2),
                                result.y + (result.height / 2))
            return True
        else:
            return False

    def tap_timeout(self, reference, target="", loop=5, timeout=5):
        if not self.enable_timeout(reference, target, loop, timeout):
            return False
        return self.tap(reference)
