import os
import logging

from bantorra.util import define
from bantorra.util import system as s

CONF_FILE = "logging.conf"
BASE_NAME = "Bantorra"
BASE_LEVEL = logging.DEBUG
BASE_FORMAT = '%(processName)s.%(name)s ( PID %(process)d ) : %(asctime)s - %(levelname)s - %(message)s'

INFO_COLOR = '\033[94m'
DEBUG_COLOR = '\033[92m'
WARNING_COLOR = '\033[93m'
ERROR_COLOR = '\033[91m'
CRITICAL_COLOR = '\033[95m'
END_COLOR = '\033[0m'


class Log(object):
    def __init__(self, name, console=True, filename="", refresh=False, shell=False):
        s.mkdir(define.APP_LOG)
        self.filename = filename
        self.logger = logging.getLogger(name)
        self.logger.setLevel(BASE_LEVEL)
        self.shell = shell
        if console:
            self.__addHandler(self.consoleHandler())
        if filename != "":
            self.__addHandler(
                self.fileHandler(os.path.normpath(
                    os.path.join(define.APP_LOG, self.filename)), refresh))

    def __addHandler(self, handler):
        self.logger.addHandler(handler)

    def consoleHandler(self):
        f = logging.Formatter(BASE_FORMAT)
        h = logging.StreamHandler()
        h.setLevel(BASE_LEVEL)
        h.setFormatter(f)
        return h

    def fileHandler(self, filename, refresh=False):
        s.touch(filename, refresh)
        fo = logging.Formatter(BASE_FORMAT)
        h = logging.FileHandler(filename, 'a+')
        h.setLevel(BASE_LEVEL)
        h.setFormatter(fo)
        return h

    def rotateFileHandler(self, filename):
        if os.path.exists(filename):
            f = logging.Formatter(BASE_FORMAT)
            h = logging.handlers.TimedRotatingFileHandler(
            filename = os.path.normpath(os.path.join(filename)),
            when = 'D',
            backupCount = 5
            )
            h.setLevel(BASE_LEVEL)
            h.setFormatter(f)
            return trh
        else:
            return None

    def debug(self, message):
        if message != None:
            if self.shell: self.logger.debug(DEBUG_COLOR + message + END_COLOR)
            else: self.logger.debug(message)

    def warning(self, message):
        if message != None:
            if self.shell: self.logger.warning(WARNING_COLOR + message + END_COLOR)
            else: self.logger.warning(message)

    def info(self, message):
        if message != None:
            if self.shell: self.logger.info(INFO_COLOR + message + END_COLOR)
            else: self.logger.info(message)

    def critical(self, message):
        if message != None:
            if self.shell: self.logger.critical(CRITICAL_COLOR + message + END_COLOR)
            else: self.logger.critical(message)

    def error(self, message):
        if message != None:
            if self.shell: self.logger.error(ERROR_COLOR + message + END_COLOR)
            else: self.logger.error(message)

    def __del__(self):
        del self

LOG = Log(BASE_NAME, filename="system.log")

if __name__ == "__main__":
    logger = LOG
    logger.debug("debug")
    logger.warning("warning")
    logger.info("info")
    logger.critical("critical")
    logger.error("error")
