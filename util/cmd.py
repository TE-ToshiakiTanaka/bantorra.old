import sys
import os
import time
import imp
import subprocess
import multiprocessing

from bantorra.util import define
from bantorra.util.log import LOG as L

TIMEOUT = 30

class Process(multiprocessing.Process):
    def __init__(self, command, queue):
        self.command = command
        self.queue = queue
        multiprocessing.Process.__init__(self)

    def run(self):
        L.info("Command Send : %s" % self.command)
        args = self.command.split(" ")
        subproc_args = { 'stdin'        : subprocess.PIPE,
                         'stdout'       : subprocess.PIPE,
                         'stderr'       : subprocess.PIPE,
        }
        try:
            proc = subprocess.Popen(args, **subproc_args)
        except OSError:
            L.info("Failed to execute command: %s" % args[0])
            sys.exit(1)
        (stdout, stderr) = proc.communicate()
        code = proc.wait()
        L.debug("Command Resturn Code: %d" % code)
        self.queue.put(stdout)

    def kill(self):
        L.debug("Kill This Process.")
        self.terminate()

class Console(object):
    def __init__(self):
        self.queue = multiprocessing.Queue()

    def __exec(self, cmd, timeout=TIMEOUT):
        proc = Process(cmd, self.queue)
        proc.start()
        proc.join(timeout)

        if proc.is_alive():
            proc.kill()
            time.sleep(3)
            L.debug("proc.terminate. %s" % proc.is_alive())

        if self.queue.empty():
            return None
        return self.queue.get()

    def execute(self, cmd, timeout=TIMEOUT):
        return self.__exec(cmd, timeout=timeout)

CONSOLE = Console()

if __name__ == "__main__":
    print CONSOLE.execute("ls -la")
