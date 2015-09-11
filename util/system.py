import os
import shutil
import tempfile
import datetime
import collections

from bantorra.util import define

def mkdir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname

def rmdir(dirname):
    if os.path.exists(dirname):
        return shutil.rmtree(dirname)

def touch(filename, refresh=False):
    d = os.path.dirname(filename)
    f = filename.split(os.sep)[-1]
    mkdir(d);
    if not os.path.exists(filename):
        tmp = open(filename, 'w')
        tmp.close()
    elif refresh:
        with open(filename, 'w') as f: pass
    return filename

def uniq(filepath):
    d = datetime.datetime.today()
    dstr = d.strftime("%Y%m%d_%H%M%S")
    filename = os.path.normpath(os.path.join(filepath, dstr))
    return touch(filename)

def rm(filename):
    if os.path.exists(filename):
        os.remove(filename)


if __name__ == "__main__":
    import time
    d = mkdir(os.path.join(define.APP_TMP, "sample"))
    time.sleep(10)
    rmdir(d)
    f = touch(os.path.join(define.APP_TMP, "hogehoge.txt"))
    time.sleep(10)
    rm(f)
