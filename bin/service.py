import os
import sys
import imp
import time
import ConfigParser

from bantorra.util import define
from bantorra.util.log import LOG as L

class ServiceControl(object):
    service = {}

    def __init__(self):
        for k in self.get_config().keys():
            self.register(k)

    def get_config(self, conf=""):
        service_conf = {}
        if conf == "":
            conf = os.path.join(define.APP_BIN, "config.ini")
        try:
            config = ConfigParser.ConfigParser()
            config.read(conf)
            for section in config.sections():
                for option in config.options(section):
                    service_conf["%s" % option] = config.get(section, option)
        except Exception as e:
            L.warning("error: could not read config file: %s" % e)
        return service_conf

    @classmethod
    def register(cls, name):
        base_dir = define.APP_BIN
        cwd = os.getcwd()
        for fdn in os.listdir(base_dir):
            if name in fdn and fdn.endswith(".py"):
                sys.path.append(base_dir)
                f, n, d = imp.find_module(name)
                module = imp.load_module(name, f, n, d)
                cls.service[name] = module.SERVICE
                sys.path.remove(base_dir)

    @classmethod
    def start_all(cls):
        try:
            for x in cls.service.values():
                x.start()
        except Exception as e:
            L.warning(str(e))

    @classmethod
    def stop_all(cls):
        try:
            for x in cls.service.values():
                x.stop()
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
    time.sleep(5)
    L.info("Stop Service")
    proc.stop_all()
