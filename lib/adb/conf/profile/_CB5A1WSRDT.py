import os
import sys

LIB_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not LIB_PATH in sys.path:
    sys.path.insert(0, LIB_PATH)

from android4_4 import Android_4_4
from xperia_sirius import Xperia_Sirius

class _CB5A1WSRDT(Android_4_4, Xperia_Sirius):
    SERIAL = "CB5A1WSRDT"
    TMP_PICTURE="CB5A1WSRDT_TMP.png"
    IP = ""
    PORT = ""

if __name__ == "__main__":
    print eval("_CB5A1WSRDT.%s" % "SERIAL")
