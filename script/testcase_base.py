import os
import sys
import argparse
import ConfigParser

import testcase_service
from bantorra.util import define
from bantorra.util.log import LOG as L

class TestCase_Base(testcase_service.TestCaseUnit):
    config = {}
    """
        TestCase_Base.
            - Parse Command Line Argument.
            - Create Service's Instance.
            - Read Config File and get value.
    """
    def __init__(self, *args, **kwargs):
        super(TestCase_Base, self).__init__(*args, **kwargs)
        self.get_config()
        self.parse()
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
        parser = argparse.ArgumentParser()
        parser.add_argument(action='store', dest='testcase',
                            help='TestCase Name.')
        parser.add_argument('-u', action='store', dest='username',
                            help='Username (E-mail) from DMM.com.')
        parser.add_argument('-p', action='store', dest='password',
                            help='Password from DMM.com.')

        parser.add_argument('-f', action='store', dest='fleet',
                            help='Fleet Number. 1 ~ 4.')
        parser.add_argument('-e', action='store', dest='expedition',
                            help='Expedition Number. 1 ~ 38.')
        parser.add_argument('-j', action='store', dest='job',
                            help='Jenkins Job Name.')
        parser.add_argument('-t', action='store', dest='timeout',
                            help='Timeout (minites.)')
        
        results = parser.parse_args()
        for k, v in vars(results).items():
            self.set("args.%s" % k, v)
        return None

    @classmethod
    def get_service(cls):
        """
            Get Service.
            in the wifi branch, Used service is there.
        """
        cls.core = cls.service["core"].get()
        cls.picture = cls.service["picture"].get()
        cls.browser = cls.service["browser"].get()

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
