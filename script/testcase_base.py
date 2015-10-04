import os
import sys
import argparse
import ConfigParser

import testcase_service
from bantorra.util import define
from bantorra.util.log import LOG as L

<<<<<<< HEAD

class TestCaseUnit(unittest.TestCase):
    service = {}
    config = {}

=======
class TestCase_Base(testcase_service.TestCaseUnit):
    config = {}
    """
        TestCase_Base.
            - Parse Command Line Argument.
            - Create Service's Instance.
            - Read Config File and get value.
    """
>>>>>>> origin/master
    def __init__(self, *args, **kwargs):
        super(TestCase_Base, self).__init__(*args, **kwargs)
        self.parse()
        self.get_config()
        self.service_check()
        self.get_service()

    @classmethod
    def set(cls, name, value):
        cls.config[name] = value
<<<<<<< HEAD

    @classmethod
    def get(cls, name):
        return cls.config[name]

    @classmethod
    def register(cls):
        base_dir = define.APP_LIB
        cwd = os.getcwd()
        for fdn in os.listdir(base_dir):
            try:
                if fdn.endswith(".pyc") or fdn.endswith(".py"):
                    pass
                else:
                    sys.path.append(os.path.join(base_dir, fdn))
                    f, n, d = imp.find_module("service")
                    module = imp.load_module("service", f, n, d)
                    cls.service[module.NAME] = module.FACTORY
                    sys.path.remove(os.path.join(base_dir, fdn))
            except Exception as e:
                L.warning('error: could not search "service.py" file in %s : %s' % (fdn, e))

    @classmethod
    def get_service(cls):
        """
            Get Service.
            in the wifi branch, Used service is there.
        """
        cls.core = cls.service["core"].get()
        cls.browser = cls.service["browser"].get()

    @classmethod
    def service_check(cls, conf=""):
        serv = cls._service_parse(conf)
        for s in serv:
            if not s in cls.service:
                L.warning("error : not installed service: %s" % s)
                sys.exit(1)
=======

    @classmethod
    def get(cls, name):
        return cls.config[name]

    def parse(self):
        """
            Parse Command Line Arguments.
        """
        return None
>>>>>>> origin/master

    @classmethod
    def get_service(cls):
        """
            Get Service.
            in the wifi branch, Used service is there.
        """
        cls.core = cls.service["core"].get()
        cls.picture = cls.service["picture"].get()

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
            config = ConfigParser.ConfigParser()
            config.read(conf)
            for section in config.sections():
                for option in config.options(section):
                    cls.config["%s.%s" % (section, option)] = config.get(section, option)
        except Exception as e:
            L.warning('error: could not read config file: %s' % e)
