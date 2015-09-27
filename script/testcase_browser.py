import os
import sys

import testcase_base

class TestCase_Base(testcase_base.TestCaseUnit):
    def __init__(self, *args, **kwargs):
        super(TestCase_Base, self).__init__(*args, **kwargs)

    def login(self, username, password):
        print self.browser.driver
