import os
import sys

LIB_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not LIB_PATH in sys.path:
    sys.path.insert(0, LIB_PATH)

from adb.module import Android


class Factory(object):
    def __init__(self):
        pass

    def get(self, profile):
        return Android(profile)

NAME = "adb"
FACTORY = Factory()

if __name__ == "__main__":
    import time
    a = FACTORY.get("84441d01zzzzzzz")
    a.reboot()
    a.root()
    a.remount()
    time.sleep(5)
    a.snapshot(a.get().TMP_PICTURE)
