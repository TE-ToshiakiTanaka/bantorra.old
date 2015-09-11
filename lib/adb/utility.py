from bantorra.util import system
from bantorra.util.cmd import CONSOLE
from bantorra.util import define
from bantorra.util.log import Log

BASE_NAME = "ADB.BobCAT"
LOGCAT_NAME = "LogCat.ADB.BobCAT"
LOGCAT_FILE = "adb_logcat.log"
LOG = Log(BASE_NAME, True, "adb.log")
LOGCAT = Log(LOGCAT_NAME, False, LOGCAT_FILE)

C = CONSOLE
S = system
APP_TMP = define.APP_TMP
APP_LOG = define.APP_LOG
