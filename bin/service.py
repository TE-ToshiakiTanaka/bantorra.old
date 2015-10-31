import os
import sys
import imp
import time
import ConfigParser
import multiprocessing

from bantorra.util import define
from bantorra.util.log import LOG as L

class ServiceControl(object):
    service = {}
    service_conf = {}

    def __init__(self):
        self.get_config()
        self.register()

    @classmethod
    def get_config(cls, conf=""):
        cls.service_conf = {}
        if conf == "":
            conf = os.path.join(define.APP_BIN, "port.ini")
            L.debug(conf)
        try:
            config = ConfigParser.ConfigParser()
            config.read(conf)
            for section in config.sections():
                for option in config.options(section):
                    cls.service_conf["%s" % option] = config.get(section, option)
        except Exception as e:
            L.warning("error: could not read config file: %s" % e)

    @classmethod
    def register(cls):
        base_dir = define.APP_BIN
        cwd = os.getcwd()
        for fdn in os.listdir(base_dir):
            try:
                if fdn.endswith(".pyc") or fdn.endswith(".py") or fdn.endswith(".ini"):
                    pass
                else:
                    sys.path.append(os.path.join(base_dir, fdn))
                    f, n, d = imp.find_module("server")
                    module = imp.load_module("server", f, n, d)
                    cls.service[module.NAME] = module
                    sys.path.remove(os.path.join(base_dir, fdn))
            except Exception as e:
                L.warning('error: could not search "server.py" file in %s : %s' % (fdn, e))

    @classmethod
    def start_all(cls):
        L.info(cls.service_conf)
        try:
            for x in cls.service.values():
                L.info(int(cls.service_conf["kancolle"]))
                #x.start(int(cls.service_conf["kancolle"]))
                p = multiprocessing.Process(target=x.start, args=(int(cls.service_conf["kancolle"]), ))
                p.daemon = True
        except Exception as e:
            L.warning(str(e))

    @classmethod
    def stop_all(cls):
        try:
            for x in cls.service.values():
                x.shutdown()
        except Exception as e:
            L.warning(str(e))

    @classmethod
    def restart_all(cls):
        cls.stop_all()
        time.sleep(3)
        cls.start_all()

if __name__ == '__main__':
    proc = ServiceControl()
    L.info("Start Service")
    proc.start_all()
    time.sleep(20)
    L.info("Stop Service")
    proc.stop_all()
