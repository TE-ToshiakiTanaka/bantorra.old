import os
import sys

LIB_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not LIB_PATH in sys.path:
    sys.path.insert(0, LIB_PATH)

from android5_1 import Android_5_1
from nexus_5 import Nexus_5

class _06ddaf4b439d3a24(Android_5_1, Nexus_5):
    SERIAL = "06ddaf4b439d3a24"
    TMP_PICTURE="06ddaf4b439d3a24_TMP.png"
    IP = ""
    PORT = ""

if __name__ == "__main__":
    print eval("_06ddaf4b439d3a24.%s" % "SERIAL")
