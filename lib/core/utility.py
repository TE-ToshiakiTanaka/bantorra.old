from bantorra.util import log
from bantorra.util import define

LOG_NAME = "Platform.Bantorra"
FILENAME = "platform.log"
APP_LIB = define.APP_LIB
APP_TMP = define.APP_TMP
APP_ROOT = define.APP_ROOT

LOG = log.Log(LOG_NAME, True, FILENAME)
