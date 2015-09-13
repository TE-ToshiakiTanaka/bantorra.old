import os

APP_UTIL = os.path.normpath(os.path.dirname(__file__))
APP_ROOT = os.path.normpath(os.path.dirname(APP_UTIL))
APP_SCRIPT = os.path.normpath(os.path.join(APP_ROOT, "script"))
APP_LIB = os.path.normpath(os.path.join(APP_ROOT, "lib"))
APP_LOG = os.path.normpath(os.path.join(APP_ROOT, "log"))
APP_TMP = os.path.normpath(os.path.join(APP_ROOT, "tmp"))
APP_BIN = os.path.normpath(os.path.join(APP_ROOT, "bin"))
APP_EXCEL = os.path.normpath(os.path.join(APP_ROOT, "excel"))
