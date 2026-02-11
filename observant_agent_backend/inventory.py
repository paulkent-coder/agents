#!/usr/bin/env python3

from .gamestate import StateModule
from .agent_config import *
from .utilities import *


class ItemManager(StateModule):
    agenda = []

    def __init__(self, state):
        self.state = state
        self.itemUnderfoot = ""
        self.itemsToNab = []
        self.notTaken = []
        self.phase = 0

    def reset(self):
        if not CONST_QUIET:
            pass
        self.itemUnderfoot = ""
        self.itemsToNab = []
        self.notTaken = []
        self.phase = 0

    def dumpCore(self):
        pass

    def displayStats(self):
        pass

    def reachForItem(self, observations, desired):
        # Look in the inventory for an item whose glyph number is
        # one of the ones in desired If one or more is found, report their
        # inventory slots and which glyph they are
        letters = []
        types = []
        indices = []
        for x in range(len(observations["inv_glyphs"])):
            for y in desired:
                if readInventoryGlyph(self.state, observations, x) == y:
                    letters.append(observations["inv_letters"][x])
                    types.append(y)
                    indices.append(x)
        return letters, types, indices

    def reachForString(self, observations, desired):
        # Look in the inventory for an item whose description contains a
        # substring in desired. If one or more is found, report their
        # inventory slots and which glyphs they are
        letters = []
        types = []
        indices = []
        for x in range(len(observations["inv_strs"])):
            for y in desired:
                if readInventoryStrs(self.state, observations, x).find(y) > -1:
                    letters.append(observations["inv_letters"][x])
                    types.append(y)
                    indices.append(x)
        return letters, types, indices

    def itemValue(self, observations, itemStr):
        # TODO
        pass

    def isWorthTaking(self, observations, itemStr):
        # TODO
        if itemStr.find("zorkmids)") != -1:
            return False  # don't bother with shops yet
        if itemStr.find("food ration") != -1:
            return True
        if itemStr.find("lichen corpse") != -1:
            return True
        if itemStr.find("lembas wafer") != -1:
            return True
        if itemStr.find(" apple") != -1:
            return True
        if itemStr.find("carrot") != -1:
            return True
        if itemStr.find("slime mold") != -1:
            return True
        if itemStr.find("meatball") != -1:
            return True
        if itemStr.find("meat stick") != -1:
            return True
        if itemStr.find("orange") != -1:
            return True
        if itemStr.find(" pear") != -1:
            return True
        if itemStr.find("melon") != -1:
            return True
        if itemStr.find("banana") != -1:
            return True
        if itemStr.find("carrot") != -1:
            return True
        if itemStr.find("cream pie") != -1:
            return True
        if itemStr.find("fortune cookie") != -1:
            return True
        if itemStr.find("cram ration") != -1:
            return True
        if itemStr.find("C-ration") != -1:
            return True
        if itemStr.find("K-ration") != -1:
            return True
        return False

    def itemDetected(self, itemStr):
        self.itemUnderfoot = itemStr

    def countUnderfoot(self, observations):
        misc = observations["misc"]
        if misc[0] or misc[1] or misc[2]:
            return -1  # wait for the dialogue box to be dismissed
        self.phase += 1
        if self.state.get("doctor").checkMajorStatus(nethack.BL_MASK_BLIND):
            # If we're blind, near-look takes a turn, which is no bueno
            return self.checkUnderfoot(observations)
        # Re-assess how many items are underfoot
        self.itemUnderfoot = ""
        return 51  # near-look

    def checkUnderfoot(self, observations):
        self.notTaken = []
        misc = observations["misc"]
        if misc[0] or misc[1] or misc[2]:
            return -1  # wait for the dialogue box to be dismissed
        # So... here is the suprisingly scary part.
        # If there are multiple items underfoot, we want to use pickup to
        # check them. That's because the pickup menu tells us the letters we
        # need to use to specify what we want. BUT, before we touch the pickup
        # key, we want to be sure there isn't exactly one item underfoot. If
        # you pickup with 0 items underfoot, it doesn't take up a turn. If you
        # pickup with 2+ items underfoot, you get the pickup menu, which can
        # be cancelled to not use a turn. (Even if you're blind – I checked.)
        # But if you pickup with exactly 1 item underfoot, you take it and
        # spend a turn. This is an observation-type function – it's not
        # supposed to do anything that causes time to elapse. I don't know
        # whether this agent is robust against a turn passing unexpectedly.
        # I wouldn't count on it – the bot probably will get desynced in some
        # way.

        # So, hopefully, we can count on being able to keep track of
        # whether exactly 1 item is underfoot.
        # That job falls on self.itemUnderfoot.
        # If it's empty, we think there isn't exactly 1 item.
        if self.itemUnderfoot != "":
            self.phase += 2
            return -1
        self.phase += 1
        # "It's heavy. Pick up anyway?" -> No
        self.state.get("queue").append(False)
        return 61  # pickup

    def readUnderfoot(self, observations):
        if readMessage(observations) != "":
            # There is currently something underfoot if and only if the
            # message is empty. If something is there, a pop-up is on screen,
            # which forces the message to be empty. If we accidentally took 1
            # thing, that gives a message and no pop-up. If there was nothing
            # there at all, that gives one of a few possible messages, and
            # no pop-up.
            # Therefore, if we see a message, there's nothing to be done.
            self.phase += 1
            return -1
        # There are at least 2 items underfoot. Let's make a note of which of
        # them are worth bothering with.
        rawDisplay = observations["tty_chars"]
        display = []
        for x in range(len(rawDisplay)):
            display.append(parse(rawDisplay[x]))
        offset = display[0].find("Pick up what?")
        if offset == -1:
            # print("Evaluating page of items beyond 1.")
            offset = display[0].find(" - ") - 1
        if offset < 0:
            offset = 0
            while display[offset] == " ":
                offset += 1
            print("Choke averted?")
            # If you need to refer to the fatal error procedure that was here,
            # it's in the version control history.
        for entry in display:
            if entry[offset:].find("(end)") != -1:
                self.phase += 1
                return 19  # close the menu
            if entry[offset:].find("(10 of ") != -1:  # FIXME
                print("\x1b[0;31mFatal error: Your lazy hack has failed you.")
                print("Implement readUnderfoot in inventory.py properly,")
                print("without relying on only single-digit page numbers.")
                # ^ This seems like a fair assumption to me, that there won't
                # be 10 pages of items on 1 square. But you never know. Might
                # as well keep tabs on that assumption.
                exit(1)
            if entry[offset+2:offset+6] == " of ":
                # We've reached a (# of #) marker. This is the end of the page.
                # This is the part you need to change if you ever find 10
                # pages of items on 1 square.
                if entry[offset+1] == entry[offset+6]:
                    # Last page. This is the real end of the items.
                    self.phase += 1
                    print("WOW that's a lotta goodies...")
                    return 19  # close the menu
                self.itemsToNab.append(keyLookup[">"])
                return 17  # next page, please
            if entry[offset+1:offset+4] != " - ":
                # empty line or category marker or something, not an item
                continue
            key = entry[offset]
            itemStr = entry[offset+4:]
            if self.isWorthTaking(observations, itemStr):
                self.itemsToNab.append(keyLookup[key])
            else:
                self.notTaken.append(itemStr)
        print("\x1b[0;31mFatal error: Improperly terminated pickup pop up...")
        print(offset)
        printScreen(observations)
        exit(1)

    def noop(self, observations):
        # We've already looked underfoot. No further action required
        return -1

    def returnToTop(self):
        self.phase = 0

    def nabGoodies(self, observations):
        if self.itemUnderfoot != "":
            if self.isWorthTaking(observations, self.itemUnderfoot):
                # print("Let's nab that.")
                self.itemUnderfoot = ""
                # "It's heavy. Pick up anyway?" -> Yes
                self.state.get("queue").append(True)
                return 61  # pickup
            return -1  # not worth bothering with
        # Let's check itemsToNab...
        toNab = self.itemsToNab
        while len(toNab) > 0 and toNab[-1] == keyLookup[">"]:
            # pop all >s off the back of itemsToNab
            # no sense going past the page with the last item that we want
            self.itemsToNab = self.itemsToNab[:len(self.itemsToNab)-1]
        if len(toNab) > 0:
            toNab.append(None)
            toNab.append(True)
            # queue up item selection key presses
            self.state.get("queue").append(toNab)
            self.itemsToNab = []
            if len(self.notTaken) == 1:
                # After picking up this stuff, there will be exactly 1 item
                # stack left.  We need to take note of this so we don't pick
                # it up immediately afterwards by mistake...
                self.itemUnderfoot = self.notTaken[0]
            # print("Let's nab at least one thing here.")
            return 61  # pickup
        return -1  # nothing worthwhile underfoot

    def update(self, observations):
        return self.agenda[self.phase](self, observations)

    agenda = [
        countUnderfoot,
        checkUnderfoot,
        readUnderfoot,
        noop
    ]


def checkUnderfoot(state, observations):
    return state.get("inventory").update(observations)


def nabGoodies(state, observations):
    return state.get("inventory").nabGoodies(observations)
