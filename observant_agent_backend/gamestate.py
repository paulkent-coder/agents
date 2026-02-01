#!/usr/bin/python

# observant_agent

from abc import ABC, abstractmethod
from .agent_config import *
from .utilities import parse, printScreen


class StateModule(ABC):
    # TODO - We probably should separate "print the obituary" and
    # "reset yourself" into different functions
    # because some parts of the obituary require collaboration
    # between modules so ideally we'd want to print everything
    # before resetting anything
    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def dumpCore(self, observations):
        pass

    @abstractmethod
    def displayStats(self):
        pass


class Gamestate(object):
    def __init__(self):
        from .behaviors import ActionQueue
        from .tracker import MonsterTracker
        from .map import Gazetteer
        from .time import Stopwatch
        from .reader import MessageSecretary
        from .doctor import StatusChecker
        from .inventory import ItemManager
        self.modules = {
            "time": Stopwatch(self),
            "queue": ActionQueue(self),
            "reader": MessageSecretary(self),
            "tracker": MonsterTracker(self),
            "map": Gazetteer(self),
            "doctor": StatusChecker(self),
            "inventory": ItemManager(self)
        }
        # self.lastKnownProtocol = ""

    def reset(self):
        for key in self.modules:
            self.modules[key].reset()
        if not CONST_QUIET:
            print("\x1b[0;0;40m----------RIP----------\x1b[0;0;0m")
        # self.lastKnownProtocol = ""

    def dumpCore(self, message, observations=None):
        if CONST_QUIET:
            return
        print("\x1b[0;31m", end="")
        print(message, end="\n\x1b[0;0m")
        # print("Last known protocol:",self.lastKnownProtocol)
        if observations != None:
            printScreen(observations)
        for key in self.modules:
            self.modules[key].dumpCore()

    def get(self, name):
        # Returns a reference to a module
        return self.modules[name]

    def displayStats(self):
        for key in self.modules:
            self.modules[key].displayStats()
