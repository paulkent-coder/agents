#!/usr/bin/env python3

from .gamestate import StateModule
from .agent_config import *
from .utilities import *

# "Permafood" = food that doesn't have an expiration date
# (and that we can't really use for any other purpose)
permafood = [1299, 2148, 2149, 2150, 2151, 2158, 2159,
             2160, 2161, 2162, 2163, 2166, 2168, 2170,
             2172, 2173, 2174, 2175, 2176]  # TODO: Add 2177 (tin)


class StatusChecker(StateModule):
    def __init__(self, state):
        self.currentAilments = []
        self.lastKnownStatus = 0
        self.lastKnownHunger = 0
        self.lastKnownEncumbrance = 0
        self.state = state
        self.printedSituation = False

        self.stats_runs = 0
        self.stats_starves = 0

    def reset(self):
        if not CONST_QUIET:
            status = self.reportStatus()
            if not len(status) == 0:
                print("Status at death: ", self.reportStatus())

        self.stats_runs += 1
        if self.lastKnownHunger >= 4:
            self.stats_starves += 1

        self.currentAilments = []
        self.lastKnownStatus = 0
        self.lastKnownHunger = 0
        self.lastKnownEncumbrance = 0
        self.printedSituation = False

    def dumpCore(self):
        status = self.reportStatus()
        if not len(status) == 0:
            print("Status at death: ", self.reportStatus())

    def displayStats(self):
        print("Proportion of runs ending in starvation:",
              (self.stats_starves / self.stats_runs))

    def recordStatus(self, observations):
        blstats = observations["blstats"]
        self.lastKnownStatus = blstats[nethack.NLE_BL_CONDITION]
        self.lastKnownHunger = blstats[nethack.NLE_BL_HUNGER]
        self.lastKnownEncumbrance = blstats[nethack.NLE_BL_CAP]

        if (not self.printedSituation) and self.lastKnownHunger >= 4:
            self.printedSituation = True
            printScreen(observations)

        return -1

    def logAilment(self, ailment):
        if (ailment not in self.currentAilments):
            self.currentAilments.append(ailment)

    def checkAilment(self, ailment):
        return ailment in self.currentAilments

    def cureAilment(self, ailment):
        self.currentAilments.remove(ailment)

    def reportStatus(self):
        result = self.currentAilments.copy()
        if (self.lastKnownStatus & nethack.BL_MASK_STONE):
            result.append("Stoning")
        if (self.lastKnownStatus & nethack.BL_MASK_SLIME):
            result.append("Sliming")
        if (self.lastKnownStatus & nethack.BL_MASK_STRNGL):
            result.append("Strangled")
        if (self.lastKnownStatus & nethack.BL_MASK_FOODPOIS):
            result.append("Food Poisoning")
        if (self.lastKnownStatus & nethack.BL_MASK_TERMILL):
            result.append("Illness")
        if (self.lastKnownStatus & nethack.BL_MASK_BLIND):
            result.append("Blindness")
        if (self.lastKnownStatus & nethack.BL_MASK_DEAF):
            result.append("Deafness")
        if (self.lastKnownStatus & nethack.BL_MASK_STUN):
            result.append("Stunning")
        if (self.lastKnownStatus & nethack.BL_MASK_CONF):
            result.append("Confusion")
        if (self.lastKnownStatus & nethack.BL_MASK_HALLU):
            result.append("Hallucination")
        if (self.lastKnownStatus & nethack.BL_MASK_LEV):
            result.append("Levitation")
        if (self.lastKnownStatus & nethack.BL_MASK_FLY):
            result.append("Flight")
        if self.lastKnownHunger == 0:
            result.append("Satiation")
        if self.lastKnownHunger == 2:
            result.append("Hunger")
        if self.lastKnownHunger == 3:
            result.append("Severe Hunger")
        if self.lastKnownHunger >= 4:
            result.append("Starvation")
        if self.lastKnownEncumbrance == 1:
            result.append("Burden")
        if self.lastKnownEncumbrance == 2:
            result.append("Stress")
        if self.lastKnownEncumbrance == 3:
            result.append("Strain")
        if self.lastKnownEncumbrance == 4:
            result.append("Overtaxing")
        if self.lastKnownEncumbrance >= 5:
            result.append("Overloading")
        return result

    def checkMajorStatus(self, status):
        return self.lastKnownStatus & status

    def fixUrgentProblems(self, observations):
        # An urgent problem is defined as one which can't wait a few turns
        # for you to kill a monster first. It might be something that
        # inhibits your ability to fight, or something that will probably
        # kill you by the time you're done.

        # Other problems go in fixMinorProblems above.
        inventory = self.state.get("inventory")
        queue = self.state.get("queue")
        hp, max = readHeroHealth(observations)
        if (hp <= 4 or max / hp >= 4):
            desired = ["potion of healing",
                       "potion of extra healing",
                       "potion of full healing",
                       "potions of healing",
                       "potions of extra healing",
                       "potions of full healing"]
            letters, _, _ = inventory.reachForString(observations, desired)
            if (len(letters) > 0):
                queue.append(False)
                queue.append(parse([letters[0]]))
                return 64  # quaff
        if self.lastKnownHunger >= 3 and self.lastKnownEncumbrance < 4:
            letters, _, _ = inventory.reachForItem(observations, permafood)
            if (len(letters) > 0):
                queue.append(False)
                queue.append(parse([letters[0]]))
                return 35  # eat
        return -1

    def fixMinorProblems(self, observations):
        inventory = self.state.get("inventory")
        if self.lastKnownHunger >= 2 and self.lastKnownEncumbrance < 4:
            letters, _, _ = inventory.reachForItem(observations, permafood)
            if (len(letters) > 0):
                self.state.get("queue").append(False)
                self.state.get("queue").append(parse([letters[0]]))
                return 35  # eat
        return -1


def checkup(state, observations):
    return state.get("doctor").recordStatus(observations)


def fixMinorProblems(state, observations):
    return state.get("doctor").fixMinorProblems(observations)


def fixUrgentProblems(state, observations):
    return state.get("doctor").fixUrgentProblems(observations)
