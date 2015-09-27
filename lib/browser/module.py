import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

LIB_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not LIB_PATH in sys.path:
    sys.path.insert(0, LIB_PATH)

from browser import utility
from browser.utility import APP_TMP
from browser.utility import APP_DRIVER
from browser.utility import DEFAULT_WAIT
from browser.utility import LOG as L

class Selenium(object):
    driver = None
    mode = "Chrome"

    def __init__(self, mode="Chrome"):
        self.__mode(mode)

    @classmethod
    def __mode(cls, mode):
        cls.mode = mode

    @classmethod
    def start(cls, url):
        if cls.mode == "FireFox":
            cls.driver = webdriver.Firefox()
        else:
            chromedriver = os.path.join(APP_DRIVER, "chromedriver.exe")
            os.environ["webdriver.chrome.driver"] = chromedriver
            cls.driver = webdriver.Chrome(chromedriver)
        cls.driver.implicitly_wait(DEFAULT_WAIT)
        cls.driver.set_window_size(1280, 720)
        cls.driver.get(url)

    @classmethod
    def screenshot(cls, filename="screen.png", host=APP_TMP):
        f = os.path.join(host, filename)
        cls.driver.save_screenshot(f)
        return f

    @classmethod
    def click(cls, element, x, y):
        #target = cls.driver.find_element_by_id(element)
        target = cls.driver.find_element_by_class_name(element)
        off_x = int(target.size["width"]) / 2
        off_y = int(target.size["height"]) / 2
        actions = ActionChains(cls.driver)
        actions.move_to_element(target)
        actions.move_by_offset(x - off_x, y - off_y)
        actions.click()
        actions.move_to_element(target)
        actions.perform()

    @classmethod
    def quit(cls):
        cls.driver.quit()

if __name__ == "__main__":
    import time
    w = Selenium()
    w.start("http://www.dmm.com/netgame/social/-/gadgets/=/app_id=854854/")
    time.sleep(10)
    w.quit()
