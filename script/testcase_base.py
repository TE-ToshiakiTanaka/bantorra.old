import os
import sys
import imp
import unittest
import ConfigParser

from bantorra.util import define
from bantorra.util.log import LOG as L


class TestCaseUnit(unittest.TestCase):
    service = {}

    def __init__(self, *args, **kwargs):
        global service
        super(TestCaseUnit, self).__init__(*args, **kwargs)
        self.service = {}
        self.register()

    @classmethod
    def register(cls):
        base_dir = define.APP_LIB
        cwd = os.getcwd()
        for fdn in os.listdir(base_dir):
            if fdn.endswith(".pyc") or fdn.endswith(".py"):
                pass
            else:
                sys.path.append(os.path.join(base_dir, fdn))
                f, n, d = imp.find_module("service")
                module = imp.load_module("service", f, n, d)
                cls.service[module.NAME] = module.FACTORY
                sys.path.remove(os.path.join(base_dir, fdn))

    @classmethod
    def service_check(cls, conf=""):
        serv = cls._service_parse(conf)
        for s in serv:
            if not s in cls.service:
                L.warning("error : not installed service: %s" % s)
                sys.exit(1)

    @classmethod
    def _service_parse(cls, conf=""):
        result = []
        if conf == "":
            conf = os.path.join(define.APP_SCRIPT, "module.ini")
        try:
            config = configparser.ConfigParser()
            config.read(conf)
            for section in config.sections():
                for option in config.options(section):
                    if config.get(section, option) == str(True):
                        result.append(option)
            return result
        except Exception as e:
            L.warning('error: could not read config file: %s' % e)
            return result

    @classmethod
    def get_config(cls, conf=""):
        """
            Get Config File.
            :arg string conf: config file path.
        """
        cls.config = {}
        if conf == "":
            conf = os.path.join(define.APP_SCRIPT, "config.ini")
        try:
            config = configparser.ConfigParser()
            config.read(conf)
            for section in config.sections():
                for option in config.options(section):
                    cls.config["%s.%s" % (section, option)] = config.get(section, option)
        except Exception as e:
            L.warning('error: could not read config file: %s' % e)

if __name__ == "__main__":
    unittest.main()
