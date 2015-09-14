import sys
import os
import argparse
import ConfigParser

import testcase_base
from bantorra.util import define
from bantorra.util.log import LOG as L

class TestCase_Base(testcase_base.TestCaseUnit):
    config = {}
    """
        TestCase_Base.
            - Parse Command Line Argument.
            - Create Service's Instance.
            - Read Config File and get value.
    """
    def __init__(self, *args, **kwargs):
        super(TestCase_Base, self).__init__(*args, **kwargs)
        self.parse()
        self.get_config()
        self.service_check()
        self.get_service()

    @classmethod
    def set(cls, name, value):
        cls.config[name] = value

    @classmethod
    def get(cls, name):
        return cls.config[name]

    def parse(self):
        """
            Parse Command Line Arguments.
        """
        return None

    @classmethod
    def get_service(cls):
        """
            Get Service.
            in the wifi branch, Used service is there.
        """
        cls.core = cls.service["core"].get()

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
