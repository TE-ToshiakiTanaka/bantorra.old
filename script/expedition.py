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

    def test_1_login(self):
        L.info("*** Login ***")
        self.assertTrue(self.kancolle_login())

    def test_2_supply(self):
        L.info("*** Supply ***")
        while self.expedition_result(): time.sleep(3)
        self.assertTrue(self.supply(self.get("args.fleet")))

    def test_3_return_home(self):
        L.info("*** Return Home ***")
        self.assertTrue(self.return_home())

    def test_4_expedition(self):
        L.info("*** Expedition ***")
        while self.expedition_result(): time.sleep(3)
        self.assertTrue(self.expedition(
            self.get("args.fleet"),
            self.get("args.expedition")))

    @classmethod
    def tearDownClass(cls):
        L.info("*** End TestCase     : %s *** " % __file__)
        cls.browser_quit()
