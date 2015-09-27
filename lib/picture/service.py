import os
import sys

LIB_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not LIB_PATH in sys.path:
    sys.path.insert(0, LIB_PATH)

from picture.module import Picture

class Factory(object):
    def __init__(self):
        pass

    def get(self):
        return Picture()

NAME = "picture"
FACTORY = Factory()

if __name__ == "__main__":
    import time
    from bantorra.util import define
    p = FACTORY.get()
    print p.find_pattern(os.path.join(define.APP_TMP, "default_TMP.png"),
                         os.path.join(define.APP_TMP, "default", "mission.png"))
