import os
import sys

import testcase_browser
import testcase_picture

from bantorra.util import define
from bantorra.util.log import LOG as L

<<<<<<< HEAD
class TestCase_Base(testcase_base.TestCaseUnit):
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

    def parse(self):
        """
            Parse Command Line Arguments.
        """
        parser = argparse.ArgumentParser(description="")
        parser.add_argument('testcase',
                            action='store',
                            type=str,
                            help='The testcase script.')
        parser.add_argument('-u', '--username',
                            action='store',
                            nargs='?',
                            type=str,
                            help='The username of dmm login. (Optional)')
        parser.add_argument('-p', '--password',
                            action='store',
                            nargs='?',
                            type=str,
                            help='The password of dmm login. (Optional)')
        args = parser.parse_args()
        for k, v in vars(args).items():
            self.set("args.%s" % k, v)

    @classmethod
    def get_config(cls, conf=""):
        """
            Get Config File.
            :arg string conf: config file path.
        """
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

    def login(self, username, password):
        print self.browser.driver
=======
class TestCase_Base(testcase_picture.TestCase_Picture,
                    testcase_browser.TestCase_Browser):
    def __init__(self, *args, **kwargs):
        super(TestCase_Base, self).__init__(*args, **kwargs)
>>>>>>> origin/master
