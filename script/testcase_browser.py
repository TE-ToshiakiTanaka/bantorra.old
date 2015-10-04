import os
import sys

import testcase_base
from bantorra.util import define
from bantorra.util.log import LOG as L

class TestCase_Browser(testcase_base.TestCase_Base):

    def browser_start(self, url):
        try:
            return self.browser.start(url)
        except Exception as e:
            L.warning(e)

    def browser_screenshot(self, filename="screen.png", host=define.APP_TMP):
        try:
            return self.browser.screenshot(filename, host)
        except Exception as e:
            L.warning(e)

    def browser_click(self, element, x, y):
        try:
            return self.browser.click(element, x, y)
        except Exception as e:
            L.warning(e)

    def browser_quit(self):
        try:
            return self.browser.quit()
        except Exception as e:
            L.warning(e)
