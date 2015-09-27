import os

from bantorra.util import define
from bantorra.util.log import Log

BASE_NAME = "Selenium.BobCAT"
LOG = Log(BASE_NAME, True, "selenium.log")

DEFAULT_WAIT = 30

APP_TMP = define.APP_TMP
APP_LOG = define.APP_LOG
APP_DRIVER = os.path.join(os.path.normpath(os.path.dirname(__file__)), "driver")
