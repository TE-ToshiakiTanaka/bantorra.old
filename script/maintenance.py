import os
import sys
import time

import testcase_normal

from bantorra.util import define
from bantorra.util.log import LOG as L

class TestCase(testcase_normal.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        # L.info("*** Start TestRunner. Version : %s" % cls.core.version())
        L.info("*** Start TestCase   : %s *** " % __file__)

    def test_1_sleep(self):
        timeout = int(self.get("args.timeout")) * 60
        L.debug("Timeout : %d " % timeout)
        time.sleep(timeout)

    @classmethod
    def tearDownClass(cls):
        L.info("*** End TestCase     : %s *** " % __file__)
