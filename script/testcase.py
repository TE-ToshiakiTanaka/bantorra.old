import os
import sys

import testcase_browser
import testcase_picture

from bantorra.util import define
from bantorra.util.log import LOG as L

class TestCase_Base(testcase_picture.TestCase_Picture,
                    testcase_browser.TestCase_Browser):
    def __init__(self, *args, **kwargs):
        super(TestCase_Base, self).__init__(*args, **kwargs)
