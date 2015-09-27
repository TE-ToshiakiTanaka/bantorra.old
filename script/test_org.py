import os
import sys
import time

import testcase

from bantorra.util import define
from bantorra.util.log import LOG as L

class TestCase(testcase.TestCase_Base):
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        L.info("*** Start TestRunner. Version : %s" % cls.core.version())
        L.info("*** Start TestCase   : %s *** " % __file__)

    def test(self):
        self.browser.start()
        self.login(self.get("args.username"), self.get("args.password"))
        self.assertTrue("kancolle" == str(self.core.version()))

    @classmethod
    def tearDownClass(cls):
        L.info("*** End TestCase     : %s *** " % __file__)
