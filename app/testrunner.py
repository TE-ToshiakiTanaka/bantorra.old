import os
import sys
import imp
import csv
import unittest
import xmlrunner

from bantorra.util import define
from bantorra.util import system as s
from bantorra.util.log import LOG as L

TIMEOUT = 1800


class TestRunner(object):
    def __init__(self):
        s.mkdir(define.APP_TMP)
        s.mkdir(define.APP_EXCEL)
        s.mkdir(define.APP_LOG)

    def load(self, testcase):
        """
            TestCase Load Method.
            .. warning::
                Default Settings, TestCase Folder is only bantorra/script.
                TestCase Class is only inheritant of testcase_base.py
            :arg string testcase: testcase name. only ".py" file.
            :return module: module object.
        """
        sys.path.append(define.APP_SCRIPT)
        if testcase.find(".py") != -1:
            script = testcase
        else:
            script = testcase + ".py"
        path = os.path.join(define.APP_SCRIPT, script)
        name = script[:script.find(".")]
        L.debug("TestCase : %s" % path)
        if os.path.exists(path):
            f, n, d = imp.find_module(str(name))
            return imp.load_module(name, f, n, d)
        else:
            return False

    def execute(self, script):
        """
            TestCase Execute Method.
            The Argument "script", choice ".py" or ".csv".
            ".py" file is executing only one testcase.
            ".csv" file is executing some testcases.
            :arg string script: testcase filename. ".py" or ".csv" file.
        """
        sys.path.append(define.APP_SCRIPT)
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()

        if script.endswith(".csv"):
            self.parse_testcase(script)
            path = define.APP_SCRIPT

            for id in self.testcase:
                files = self.search_testcase(id)
                if not files: pass
                else:
                    module = self.load(files)
                    if not module: pass
                    else: suite.addTest(loader.loadTestsFromModule(module))
            xmlrunner.XMLTestRunner(output=define.APP_REPORT).run(suite)
        else:
            module = self.load(script)
            if not module: pass
            else: suite.addTest(loader.loadTestsFromModule(module))
            unittest.TextTestRunner(verbosity=2).run(suite)

    def search_testcase(self, id, folder=define.APP_SCRIPT):
        """
            Testcase Search Method.
            :arg string id: testcase id. ex.) 412229
            :arg string folder: testcase exists folder. Default : bantorra/script
            :return string: filename. or False.
        """
        files = os.listdir(define.APP_SCRIPT)
        for filename in files:
            path, ext = os.path.splitext(filename)
            if id in filename and ext == ".py":
                return filename
        return False

    def parse_testcase(self, filename, folder=define.APP_EXCEL):
        """
            Parse TestCases in the ".csv" File.
            :arg string filename: csv filename.
            :arg string folder: exists csv file. Default : bantorra/excel
        """
        self.testcase = []
        try:
            path, ext = os.path.splitext(filename)
            if ext != ".csv": pass
            else:
                with open(os.path.join(folder, filename), 'r') as f:
                    reader = csv.reader(f)
                    next(reader)
                    for r in reader: self.testcase.append(r[0])
        except Exception, e:
            L.warning('error: could not read config file: %s' % e)
            return

if __name__ == "__main__":
    runner = TestRunner()
    if len(sys.argv[1:]) < 1:
        sys.exit("Usage: %s <filename>" % sys.argv[0])
    testcase = sys.argv[1]
    L.info("testcase name : %s " % testcase)
    runner.execute(testcase)
