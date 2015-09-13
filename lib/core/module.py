import os
import sys
import platform
from git import Repo

LIB_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not LIB_PATH in sys.path:
    sys.path.insert(0, LIB_PATH)

from core import utility
from core.utility import LOG as L

class Platform(object):
    def __init__(self):
        pass

    def version(self):
        repo = Repo(utility.APP_ROOT)
        return repo.active_branch

    def python_info(self):
        result = {}
        result["version"] = platform.python_version()
        result["compiler"] = platform.python_compiler()
        result["build"] = platform.python_build()
        result["implementation"] = platform.python_implementation()
        result["branch"] = platform.python_branch()
        return result

if __name__ == "__main__":
    p = Platform()
    print(p.version())
    print(p.python_info())
