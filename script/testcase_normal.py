import os
import sys
import time

import testcase

from bantorra.util import define
from bantorra.util.log import LOG as L

class TestCase(testcase.TestCase_Base):
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)

    def kancolle_login(self):
        self.browser_start(self.get("dmm.url"))
        self.browser_login()
        if not self.enable_timeout("login.png"): return False
        time.sleep(3)
        self.tap_timeout("login.png", self.get("player.capture"))
        time.sleep(1)
        return self.enable_timeout("home.png")

    def expedition_result(self):
        if self.enable_timeout("expedition_result.png"):
            self.tap("expedition_result.png", self.get("player.capture"))
            time.sleep(5)
            self.tap_timeout("next.png"); time.sleep(1)
            self.tap_timeout("next.png"); time.sleep(1)
            return self.enable_timeout("expedition_result.png", loop=3, timeout=2)
        else:
            return False

    def supply(self, fleet):
        if not self.enable_timeout("home.png"):
            return False
        self.tap("supply.png"); time.sleep(1)
        self.tap(self.__fleet(fleet)); time.sleep(1)
        if not self.enable_timeout(self.__fleet_focus(fleet)):
            return False
        while self.tap_timeout("supply_check.png", loop=3, timeout=2): time.sleep(2)
        self.tap_timeout("supply_decide.png")
        return self.enable_timeout("supply_done.png")

    def expedition(self, fleet, id):
        if not self.enable_timeout("home.png"):
            return False
        self.tap("sortie.png"); time.sleep(1)
        self.tap_timeout("expedition.png"); time.sleep(1)
        self.__expedition_stage(id)
        self.tap_timeout(self.__expedition_id(id)); time.sleep(1)
        self.tap_timeout("expedition_decide.png"); time.sleep(1)
        if not self.enable_timeout(self.__fleet_focus(fleet)):
            self.tap(self.__fleet(fleet)); time.sleep(1)
        if self.enable_timeout("expedition_done.png"):
            return False
        self.tap_timeout("expedition_start.png")
        if self.enable_timeout("expedition_done.png"):
            return self.enable_timeout(self.__fleet_focus(fleet)) \
                or self.enable_timeout(self.__fleet_focus_focus(fleet))
        else:
            return False

    def __expedition_stage(self, id):
        if int(id) > 32: self.tap_timeout("expedition_stage_5.png"); time.sleep(1)
        elif int(id) > 24: self.tap_timeout("expedition_stage_4.png"); time.sleep(1)
        elif int(id) > 16: self.tap_timeout("expedition_stage_3.png"); time.sleep(1)
        elif int(id) > 8: self.tap_timeout("expedition_stage_2.png"); time.sleep(1)
        else: pass

    def return_home(self):
        self.tap_timeout("return_home.png"); time.sleep(1)
        return self.enable_timeout("home.png")

    def __fleet(self, fleet):
        return "fleet_%s.png" % fleet

    def __fleet_focus(self, fleet):
        return "fleet_%s_focus.png" % fleet

    def __fleet_focus_focus(self, fleet):
        return "fleet_%s_focus_focus.png" % fleet

    def __expedition_id(self, id):
        return "expedition_%s.png" % id

    def __mission_category(self, category):
        if category == "expedition": return "expedition"
        elif category == "exercises": return "exercises"
        elif category == "docking": return "docking"
        elif category == "sally": return "sally"
        else: return "expedition"

    def __mission_id(self, category, id):
        return "mission_%s_%s.png" % (self.__mission_category(category), id)

    def __mission_done_id(self, category, id):
        return "mission_%s_%s_done.png" % (self.__mission_category(category), id)

    def __stage(self, stage):
        return "stage_%s.png" % stage

    def __area(self, stage, area):
        return "area_%s_%s.png" % (stage, area)
