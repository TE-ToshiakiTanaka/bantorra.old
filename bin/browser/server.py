import tornado.ioloop
import tornado.web
import tornado.escape
import tornado.httpserver
import tornado.options

from tornado.options import define, options

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import os
from bantorra.util.define import APP_TMP
from bantorra.util.log import LOG as L

define("port", default=5000, type=int)

APP_DRIVER = os.path.join(os.path.normpath(os.path.dirname(__file__)), "driver")
DEFAULT_WAIT = 30

class Application(tornado.web.Application):
    driver = None
    mode = "Chrome"

    def __init__(self, url, mode=None):
        handlers = [
            (r'/click', ClickHandler),
            (r'/screenshot', ScreenShotHandler),
            (r'/quit', QuitHandler),
        ]
        settings = dict(
            autoescape="xhtml_escape",
            debug=True,
        )

        if self.mode == "FireFox":
            self.driver = webdriver.Firefox()
        else:
            chromedriver = os.path.join(APP_DRIVER, "chromedriver.exe")
            os.environ["webdriver.chrome.driver"] = chromedriver
            self.driver = webdriver.Chrome(chromedriver)
        self.driver.implicitly_wait(DEFAULT_WAIT)
        self.driver.set_window_size(1280, 720)
        self.driver.get(url)

        tornado.web.Application.__init__(self, handlers, **settings)

    def __del__(self):
        self.driver.quit()

class BaseHandler(tornado.web.RequestHandler):

    def screenshot(self, filename="screen.png", host=APP_TMP):
        f = os.path.join(host, filename)
        self.application.driver.save_screenshot(f)
        return f

    def click(self, element, x, y):
        #target = cls.driver.find_element_by_id(element)
        target = self.application.driver.find_element_by_class_name(element)
        off_x = int(target.size["width"]) / 2
        off_y = int(target.size["height"]) / 2
        actions = ActionChains(self.application.driver)
        actions.move_to_element(target)
        actions.move_by_offset(x - off_x, y - off_y)
        actions.click()
        actions.move_to_element(target)
        actions.perform()

    def quit(self):
        self.application.driver.quit()

class LoginHandler(BaseHandler):
    def post(self):
        try:


class ClickHandler(BaseHandler):
    def post(self):
        try:
            x = int(self.get_argument("x"))
            y = int(self.get_argument("y"))
            element = int(self.get_argument("element"))
            self.click(element, x, y)
            return self.write({"success":True})
        except Exception as e:
            L.warning(e)
            return self.write({"success":False})

class ScreenShotHandler(BaseHandler):
    def post(self):
        try:
            filename = self.get_argument("filename")
            L.debug(self.screenshot(filename=filename))
            return self.write({"success":True})
        except Exception as e:
            L.warning(e)
            return self.write({"success":False})

class QuitHandler(BaseHandler):
    def post(self):
        try:
            self.quit()
            return self.write({"success":True})
        except Exception as e:
            L.warning(e)
            return self.write({"success":False})

def main(url, mode="Chorme"):
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(url, mode))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main("http://www.google.com")
