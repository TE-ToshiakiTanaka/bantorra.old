import os
import sys

LIB_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not LIB_PATH in sys.path:
    sys.path.insert(0, LIB_PATH)

from core.module import Platform

class Factory(object):
    def __init__(self):
        pass

    def get(self):
        return Platform()


NAME = "core"
FACTORY = Factory()

if __name__ == "__main__":
    p = FACTORY.get()
    print(p.version())
    print(p.python_info())
