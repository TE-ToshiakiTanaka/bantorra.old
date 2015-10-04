import os
import sys

LIB_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not LIB_PATH in sys.path:
    sys.path.insert(0, LIB_PATH)

from browser.module import Selenium

class Factory(object):
    def __init__(self):
        pass

    def get(self, mode="Chrome"):
        return Selenium(mode)

NAME = "browser"
FACTORY = Factory()

if __name__ == "__main__":
    import time
    w = FACTORY.get()
    w.start("http://www.dmm.com/netgame/social/-/gadgets/=/app_id=854854/")
    time.sleep(5)
    w.quit()
