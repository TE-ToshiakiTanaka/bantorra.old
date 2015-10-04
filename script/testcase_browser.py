import os
import sys

import testcase_base

from bantorra.util import define
from bantorra.util.log import LOG as L

class TestCase_Browser(testcase_base.TestCase_Base):

    @classmethod
    def browser_start(cls, url):
        try:
            return cls.browser.start(url)
        except Exception as e:
            L.warning(e)

    @classmethod
    def browser_screenshot(cls, filename="screen.png", host=define.APP_TMP):
        try:
            return cls.browser.screenshot(filename, host)
        except Exception as e:
            L.warning(e)

    @classmethod
    def browser_click(cls, element, x, y):
        try:
            return cls.browser.click(element, x, y)
        except Exception as e:
            L.warning(e)

    @classmethod
    def browser_quit(cls):
        try:
            return cls.browser.quit()
        except Exception as e:
            L.warning(e)
