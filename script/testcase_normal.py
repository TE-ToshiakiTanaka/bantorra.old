import os
import sys
import time

import testcase

from bantorra.util import define
from bantorra.util.system import POINT
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
        self.tap_timeout("supply_check.png", loop=3, timeout=2)
        while self.enable_timeout("supply_done.png", loop=3, timeout=2):
            if self.enable_timeout("cat.png", loop=3, timeout=2): break
            self.tap_timeout("supply_check.png", loop=3, timeout=2)
            time.sleep(2)
        return not self.enable_timeout("supply_done.png", loop=3, timeout=2)

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
            return True
        self.tap_timeout("expedition_start.png")
        if self.enable_timeout("expedition_done.png"):
            return self.enable_timeout(self.__fleet_focus(fleet)) \
                or self.enable_timeout(self.__fleet_focus_focus(fleet))
        else:
            return False

    def mission(self):
        if not self.enable_timeout("home.png"):
            return False
        for i in xrange(5):
            self.tap_timeout("mission.png", loop=3, timeout=1); time.sleep(1)
            if not self.enable("home.png"): break
            else:
                self.tap_coordinate(785, 125); time.sleep(1)
                if not self.enable("home.png"): break
        if self.enable_timeout("home.png", loop=2, timeout=2): return False
        if self.tap_timeout("mission_oyodo.png"): time.sleep(1)
        else: self.tap_coordinate(784, 295); time.sleep(1)
        sally=1; expedition=1; docking=1; exercises=1
        while True:
            self.browser_capture(self.get("player.capture"))
            while self.tap_timeout("mission_done.png", loop=2, timeout=2):
                time.sleep(2)
                self.tap_timeout("mission_done_done.png", loop=2, timeout=2)
                if self.enable_timeout("cat.png", loop=3, timeout=2): break
            sally = self.__mission_sally(self.get("player.capture"), id=sally)
            expedition = self.__mission_expedition(self.get("player.capture"), id=expedition)
            docking = self.__mission_docking(self.get("player.capture"), id=docking)
            exercises = self.__mission_exercises(self.get("player.capture"), id=exercises)
            if not self.tap_timeout("mission_next.png"): break
            if self.enable_timeout("cat.png", loop=3, timeout=2): break
        return True

    def exercises(self):
        if not self.enable_timeout("home.png"):
            return False
        self.tap("sortie.png"); time.sleep(1)
        self.tap_timeout("exercises.png"); time.sleep(1)
        p = POINT(int(self.get("position.exercises_x")),
                  int(self.get("position.exercises_y")),
                  int(self.get("position.exercises_width")),
                  int(self.get("position.exercises_height")))
        for i in xrange(5):
            p.y = p.y + p.height
            if self.enable_timeout_crop_box(
                "exercises_win.png", p, loop=3, timeout=1):
                L.debug("I'm already fighting. I won.")
            elif self.enable_timeout_crop_box(
                "exercises_lose.png", p, loop=3, timeout=1):
                L.debug("I'm already fighting. I lost.")
            else:
                self.tap_coordinate(
                    (p.x + p.width / 2), (p.y + p.height / 2)); time.sleep(1)
                self.tap_timeout(
                    "exercises_attack.png", loop=3, timeout=1); time.sleep(1)
                if not self.tap_timeout(
                    "exercises_start.png", loop=3, timeout=1):
                    return False
                time.sleep(1)
                while not self.enable_timeout("next.png", loop=3, timeout=2):
                    if self.enable_timeout("cat.png", loop=3, timeout=2): break
                    if self.tap("battle_formation.png"): time.sleep(1)
                    if self.tap("night_warfare_start.png"): time.sleep(1)
                    time.sleep(10)
                while self.tap_timeout("next.png", loop=3, timeout=2):
                    if self.enable_timeout("cat.png", loop=3, timeout=2): break
                    time.sleep(5)
                return self.enable_timeout("home.png")

    def docking(self):
        if not self.enable_timeout("home.png"): return False
        self.tap("docking.png"); time.sleep(5)
        for i in xrange(3):
            position = self.find("docking_room.png")
            if position == None: break
            self.tap_timeout("docking_room.png", self.get("player.capture"))
            time.sleep(5); result = self.__docking()
            self.tap_coordinate(
                int(position.x + position.width / 2),
                int(position.y + position.height / 2))
            if not result: return True
        return True

    def __docking(self):
        if not self.enable_timeout("docking_next.png", loop=3, timeout=2):
            return False
        p = POINT(int(self.get("position.dock_ship_x")),
                  int(self.get("position.dock_ship_y")) - int(self.get("position.dock_ship_height")),
                  int(self.get("position.dock_ship_width")),
                  int(self.get("position.dock_ship_height")))
        for i in xrange(10):
            p.y = p.y + p.height
            self.tap_coordinate(
                (p.x + p.width / 2), (p.y + p.height / 2)); time.sleep(1)
            time.sleep(1)
            if self.tap_timeout("docking_start.png", loop=1, timeout=1):
                if self.tap_timeout("docking_yes.png", loop=2, timeout=1):
                    time.sleep(5); return True
            self.tap_coordinate(
                (p.x + p.width / 6), (p.y + p.height / 2)); time.sleep(1)
        return False

    def sally(self, fleet, stage, area):
        if not self.enable_timeout("home.png"): return False
        self.tap("sortie.png"); time.sleep(1)
        self.tap_timeout("sally.png"); time.sleep(1)
        self.tap_timeout(self.__stage(stage)); time.sleep(1)
        self.tap_timeout(self.__area(stage, area)); time.sleep(1)
        self.tap_timeout("expedition_decide.png", loop=3, timeout=2); time.sleep(1)
        if not self.enable_timeout(self.__fleet_focus(fleet), loop=3, timeout=2):
            self.tap_timeout(self.__fleet(fleet)); time.sleep(1)
        self.tap_timeout("sally_start.png")
        return self.enable_timeout("compass.png", loop=5, timeout=5)


    def battle(self):
        if not self.enable_timeout("compass.png"):
            return False
        while not self.enable_timeout("next.png", loop=3, timeout=2):
            if self.enable_timeout("cat.png", loop=3, timeout=2): break
            if self.tap("compass.png", self.get("player.capture")):
                time.sleep(1); self.browser_capture(self.get("player.capture"))
            if self.tap("battle_formation.png", self.get("player.capture")):
                time.sleep(1); self.browser_capture(self.get("player.capture"))
            if self.tap("night_warfare_start.png", self.get("player.capture")):
                time.sleep(1); self.browser_capture(self.get("player.capture"))
            time.sleep(10)
        while self.tap_timeout("next.png", loop=3, timeout=2):
            if self.enable_timeout("cat.png", loop=3, timeout=2): break
            time.sleep(5)
        while not self.enable_timeout("withdrawal.png", loop=3, timeout=2):
            if self.enable_timeout("cat.png", loop=3, timeout=2): break
            if self.tap("return.png", self.get("player.capture")):
                time.sleep(1); self.browser_capture(self.get("player.capture"))
            time.sleep(10)
        self.tap_timeout("withdrawal.png"); time.sleep(1)
        return self.enable_timeout("home.png")

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

    def __mission_sally(self, capture, id=1):
        done = id
        for i in xrange(int(id), 4):
            if self.enable(self.__mission_id("sally", i), capture):
                if not self.enable_timeout_crop(
                    self.__mission_id("sally", i),
                    "mission_receipt.png",
                    filename=self.get("player.capture"),
                    loop=1, timeout=1):
                    if self.tap(self.__mission_id("sally", i),
                                target=self.get("player.capture")):
                        time.sleep(1); done = i
        return done

    def __mission_expedition(self, capture, id=1):
        done = id
        for i in xrange(int(id), 4):
            if self.enable(self.__mission_id("expedition", i), capture):
                if not self.enable_timeout_crop(
                    self.__mission_id("expedition", i),
                    "mission_receipt.png",
                    filename=self.get("player.capture"),
                    loop=1, timeout=1):
                    if self.tap(self.__mission_id("expedition", i),
                                target=self.get("player.capture")):
                        time.sleep(1); done = i
        return done

    def __mission_docking(self, capture, id=1):
        done = id
        for i in xrange(int(id), 3):
            if self.enable(self.__mission_id("docking", i), capture):
                if not self.enable_timeout_crop(
                    self.__mission_id("docking", i),
                    "mission_receipt.png",
                    filename=self.get("player.capture"),
                    loop=1, timeout=1):
                    if self.tap(self.__mission_id("docking", i),
                                target=self.get("player.capture")):
                        time.sleep(1); done = i
        return done

    def __mission_exercises(self, capture, id=1):
        done = id
        for i in xrange(int(id), 3):
            if self.enable(self.__mission_id("exercises", i), capture):
                if not self.enable_timeout_crop(
                    self.__mission_id("exercises", i),
                    "mission_receipt.png",
                    filename=self.get("player.capture"),
                    loop=1, timeout=1):
                    if self.tap(self.__mission_id("exercises", i),
                                target=self.get("player.capture")):
                        time.sleep(1); done = i
        return done

    def __stage(self, stage):
        return "stage_%s.png" % stage

    def __area(self, stage, area):
        return "area_%s_%s.png" % (stage, area)
