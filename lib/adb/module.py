import os
import sys
import imp
import time
import threading
import subprocess

LIB_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not LIB_PATH in sys.path:
    sys.path.insert(0, LIB_PATH)

PROFILE_PATH = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "conf", "profile"))
if not PROFILE_PATH in sys.path:
    sys.path.insert(0, PROFILE_PATH)

from adb import utility
from adb.utility import C
from adb.utility import LOG as L
from adb.utility import LOGCAT as LC

TIMEOUT = 30


class AndroidBase(object):
    def __init__(self, profile):
        self.WIFI = False
        self._set_profile(profile)

    def _set_profile(self, name):
        class_name = "_" + name
        for fdn in os.listdir(PROFILE_PATH):
            try:
                if fdn.endswith("__init__.py"):
                    pass
                elif fdn.endswith(".py") and (name in fdn):
                    prof = fdn.replace(".py", "")
                    f,n,d = imp.find_module(str(prof))
                    module = imp.load_module(prof,f,n,d)
                    self.profile = getattr(module, class_name)
                    self.profile.SERIAL = name
            except Exception as e:
                L.debug('=== Error Exception ===')
                L.debug('type     : ' + str(type(e)))
                L.debug('args     : ' + str(e.args))
                L.debug('message  : ' + e.message)
                L.debug('e        : ' + str(e))

    def get_profile(self):
        return self.profile

    def __exec(self, cmd, timeout=TIMEOUT):
        return C.execute(cmd, timeout=timeout).decode("utf-8")

    def _target(self):
        if not self.WIFI:
            return "-s %s " % (self.profile.SERIAL)
        else:
            return "-s %s:%s " % (self.profile.IP, self.profile.PORT)

    def _adb(self, cmd, timeout=TIMEOUT):
        if "adb" in cmd:
            L.debug("command include [adb]. : %s" % cmd)
        cmd = "adb %s" % cmd
        return self.__exec(cmd, timeout)

    def push(self, src, dst):
        L.debug("[push]. : %s -> %s" % (src, dst))
        cmd = "%spush %s %s" % (self._target(), src, dst)
        return self._adb(cmd)

    def pull(self, src, dst):
        L.debug("[pull]. : %s -> %s" % (src, dst))
        cmd = "%spull %s %s" % (self._target(), src, dst)
        return self._adb(cmd)

    def shell(self, cmd, timeout=TIMEOUT):
        if "shell" in cmd:
            L.debug("command include [shell]. : %s" % cmd)
        cmd = "%sshell %s" % (self._target(), cmd)
        return self._adb(cmd, timeout)

    def kill(self):
        cmd = "kill-server"
        return self._adb(cmd)

    def connect(self):
        if self.WIFI:
            cmd = "connect %s:%s" % (self.profile.IP, self.profile.PORT)
            return self._adb(cmd)

    def disconnect(self):
        if self.WIFI:
            cmd = "disconnect %s:%s" % (self.profile.IP, self.profile.PORT)
            return self._adb(cmd)

    def usb(self):
        if self.WIFI:
            self.disconnect()
            self.WIFI = False
        cmd = "%susb" % (self._target())
        return self._adb(cmd)

    def tcpip(self):
        if not self.WIFI:
            self.disconnect()
            self.WIFI = True
        cmd = "tcpip %s" % (self.profile.PORT)
        return self._adb(cmd)

    def root(self):
        cmd = "%sroot " % self._target()
        L.debug(str(self._adb(cmd)))
        self.kill()
        if self.WIFI: self.tcpip()
        else: self.usb()
        self.connect()

    def remount(self):
        cmd = "%sremount " % self._target()
        L.debug(self._adb(cmd))

    def restart(self):
        cmd = "%sreboot" % self._target()
        L.debug(self._adb(cmd))

    def install(self, application, timeout=TIMEOUT):
        cmd = "%sinstall -r %s" % (self._target(), application)
        L.debug(self._adb(cmd, timeout))

    def uninstall(self, application):
        cmd = "%suninstall %s" % (self._target(), application)
        L.debug(self._adb(cmd))

    def adb(self, cmd, timeout=TIMEOUT):
        if "adb" in cmd:
            L.debug("command include [adb]. : %s" % cmd)
        cmd = "%s %s" % (self._target(), cmd)
        return self._adb(cmd, timeout)

class AndroidLogCatReader(threading.Thread):
    """
        This class is not Interface of Android Module.
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def set_fd(self, fd):
        assert callable(fd.readline)
        self._fd = fd

    def run(self):
        for line in iter(self._fd.readline, ''):
            LC.debug(line.decode('utf-8').rstrip())

    def eof(self):
        return not self.is_alive()

    def kill(self):
        self.terminate()

class AndroidLogCat(object):
    def __init__(self, adb):
        self._adb = adb
        self.stdout_reader = AndroidLogCatReader()

    def start(self):
        logcat_file = os.path.join(utility.APP_LOG, utility.LOGCAT_FILE)
        f = open(logcat_file, "w"); f.close()
        clear = "%slogcat -c" % (self._adb._target())
        self._adb._adb(clear)
        cmd = "adb %slogcat" % (self._adb._target())
        args = cmd.split(" ")
        self.proc = subprocess.Popen(args, stdout=subprocess.PIPE)

        self.stdout_reader.set_fd(self.proc.stdout)
        self.stdout_reader.start()

    def kill(self):
        L.debug("Kill This Process.")
        self.proc.terminate()

class Android(object):
    def __init__(self, profile):
        self._adb = AndroidBase(profile)
        self._logcat = AndroidLogCat(self._adb)

    def connect(self, type="USB"):
        if type == "WIFI":
            self._adb.tcpip()
            self._adb.connect()
        else : self._adb.usb()

    def start_logcat(self):
        """
            Starting the Logcat.
            .. note::
                Default Output File : bobcat/log/logcat.log.
        """
        self._logcat.start()

    def stop_logcat(self):
        """
            Stopping the Logcat.
        """
        self._logcat.kill()

    def push(self, local, remote):
        """
            Copies a specified file from local to remote.
            :arg string local: Local file. Selected full path.
            :arg string remote: Remote Path. ex.) /data/local/tmp
            :return string: adb result.
        """
        return self._adb.push(local, remote)

    def pull(self, remote, local):
        """
            Pull a specitied file from remote to local.
            :arg string remote: Remote File Path. Selected full path.
            :arg string local: Local Path.
            :return string: adb result.
        """
        return self._adb.pull(remote, local)

    def snapshot(self, filename, host=utility.APP_TMP):
        """
            Get SnapShot. Image Format is PNG.
            :arg string filename: Screenshot Filename.
            :arg string host: Save Path at the local. Default: bobcat/tmp/* .
            :return string: local file path.
        """
        cmd = "screencap -p /sdcard/%s" % (filename)
        self._adb.shell(cmd)
        remote = "/sdcard/%s" % (filename)
        self._adb.pull(remote, host)
        cmd = "rm /sdcard/%s" % (filename)
        self._adb.shell(cmd)
        return os.path.join(host, filename)

    def install(self, cmd, timeout=TIMEOUT):
        """
            Install APK File.
            :arg string cmd: install apk package file path.
            :arg string timeout: timeout. default: 30sec.
            :return string: adb result.
        """
        return self._adb.install(cmd, timeout)

    def uninstall(self, cmd):
        """
            Uninstall APK File.
            :arg string cmd: uninstall apk package name.
            :return string: adb result.
        """
        package = cmd.split("/")[0]
        return self._adb.uninstall(package)

    def shell(self, cmd):
        """
            Interface of Android Shell Command.
            :arg string cmd: command. ex.) dumpsys wifi
            :return string: adb result.
        """
        return self._adb.shell(cmd)

    def input(self, cmd):
        """
            Interface of Android Input Command.
            :arg string cmd: command.
            :return string: adb result.
        """
        if "input" in cmd:
            L.debug("command include [input]. : %s" % cmd)
        cmd = "input %s" % cmd
        return self._adb.shell(cmd)

    def am(self, cmd):
        """
            Interface of Android 'am' Command.
            :arg string cmd: android command.
            :return string: adb result
        """
        if "am" in cmd:
            L.debug("command include [am]. : %s" % cmd)
        cmd = "am %s" % cmd
        return self._adb.shell(cmd)

    def getprop(self, prop):
        """
            Interface of Android 'getprop' Command.
            :arg string prop: property name. ex) ro.secure
            :return string: adb result.
        """
        if "getprop" in prop:
            L.debug("command include [getprop]. : %s" % prop)
        cmd = "getprop %s" % prop
        return self._adb.shell(cmd)

    def setprop(self, prop, value):
        """
            Interface of Android 'setprop' Command.
            :arg string prop: property name
            :arg string value: property value
            :return string: adb result.
        """
        if "setprop" in prop:
            L.debug("command include [setprop]. : %s" % prop)
        cmd = "setprop %s %s" % (prop, value)
        return self._adb.shell(cmd)

    def root(self):
        return self._adb.root()

    def remount(self):
        L.info(self._adb.remount());time.sleep(5)

    def tap(self, x, y):
        cmd = "tap %d %d" % (x,y)
        return self.input(cmd)

    def swipe_(self, x1, y1, x2, y2):
        cmd = "swipe %d %d %d %d" % (x1, y1, x2, y2)
        return self.input(cmd)

    def keyevent(self, code):
        cmd = "keyevent %s " % (code)
        return self.input(cmd)

    def enable(self, app):
        package = app.split("/")[0]
        cmd = "pm enable %s" % (package)
        return self.shell(cmd)

    def disable(self, app):
        package = app.split("/")[0]
        cmd = "pm disable-user %s" % (package)
        return self.shell(cmd)

    def invoke(self, app):
        cmd = "start -n %s" % (app)
        return self.am(cmd)

    def intent(self, category, contents, mine):
        cmd = 'start -a android.intent.action.VIEW -d %s%s -t %s' \
            % (category, contents, mine)
        return self.am(cmd)

    def web(self, contents):
        cmd = 'start -a android.intent.action.VIEW -d "%s"' % (contents)
        return self.am(cmd)

    def text(self, cmd):
        args = cmd.split(" ")
        if len(args) == 1: self._text(args[0])
        else:
            for arg in args:
                self._text(arg)
                self.keyevent(self.get().KEYCODE_SPACE)

    def _text(self, cmd):
        if "text" in cmd:
            L.debug("command include [text]. : %s" % cmd)
        cmd = "text %s" % cmd
        return self.input(cmd)

    def get(self):
        return self._adb.get_profile()

    def stop(self, app):
        package = app.split("/")[0]
        cmd = "am force-stop %s " % (package)
        return self._adb.shell(cmd)

    def power(self):
        self.keyevent(self.get().KEYCODE_POWER)

    def boot_completed(self):
        return self.getprop(self.get().PROP_BOOT_COMPLETED).replace("\r","").replace("\n","") == "1"

    def reboot(self):
        self._adb.restart()
        time.sleep(20)
        self._adb.usb()
        while not self.boot_completed():
            time.sleep(5)


if __name__ == '__main__':
    a = Android("84441d01zzzzzzz")
    a.reboot()
    a.root()
    a.remount()
    time.sleep(5)
    a.snapshot(a.get().TMP_PICTURE)
