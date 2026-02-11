#!/usr/bin/python

from .names import monsterNames, reservedNames
from .gamestate import StateModule
from .utilities import *
import random
from nle import nethack as nh


class LogbookEntry(object):
    def __init__(self):
        self.pos = []  # row, then col
        self.glyph = -1
        self.turnLastSeen = -1
        # 1 = hostile, 0 = peaceful, -1 = tame;
        # maybe we can even use this to track tameness value?
        self.hostility = 1

    def updatePos(self, pos, observations):
        self.pos = pos
        self.turnLastSeen = readTurn(observations)

    def setGlyph(self, glyph):
        realGlyph = glyph
        if realGlyph >= 381 and realGlyph < 762:
            # This is a pet; pets get different glyphs for some reason.
            # But, the glyphs are in the same order, so subtracting 381
            # gives us the monster type, which is what we care about.
            realGlyph -= 381
            self.hostility = -1
        self.glyph = realGlyph


class MonsterTracker(StateModule):
    agenda = []

    def __init__(self, state):
        self.names = monsterNames.copy()
        random.shuffle(self.names)  # variety is the spice of life
        self.names += reservedNames
        self.lookup = {}
        self.database = []
        for x in range(len(self.names)):
            self.lookup[self.names[x]] = x
            self.database.append(LogbookEntry())
        self.phase = 0
        self.nextOpenName = 0
        self.toName = []
        # parallel array to toName;
        # notes whether a newly-spotted monster is hostile
        self.stances = []
        self.state = state
        self.visibleMonsters = {}

        self.stats_runs = 0
        self.stats_names = 0
        self.stats_monsters = 0

    def reset(self):
        if not CONST_QUIET:
            print(self.nextOpenName, "names assigned to monsters.")
            numMons = len(self.visibleMonsters)
            print(numMons, "monsters visible when the agent died.")

        self.stats_runs += 1
        self.stats_names += self.nextOpenName
        self.stats_monsters += len(self.visibleMonsters)

        self.names = self.names[:len(monsterNames)]
        random.shuffle(self.names)
        self.names += reservedNames
        self.database = []
        for x in range(len(self.names)):
            self.lookup[self.names[x]] = x
            self.database.append(LogbookEntry())
        self.phase = 0
        self.nextOpenName = 0
        self.toName = []
        self.stances = []
        self.visibleMonsters = {}

    def dumpCore(self):
        pass

    def displayStats(self):
        averageNames = self.stats_names / self.stats_runs
        averageMonsters = self.stats_monsters / self.stats_runs
        print("Average number of names assigned:", averageNames)
        print("Average number of monsters visible at death:", averageMonsters)

    def update(self, observations):
        return self.agenda[self.phase](self, observations)

    def look(self, observations):
        misc = observations["misc"]
        if misc[0] or misc[1] or misc[2]:
            return -1  # wait for the dialogue box to be dismissed
        self.visibleMonsters = {}
        self.phase += 1
        # "What do you want to look at?" -> All monsters on map
        self.state.get("queue").append(55)
        return 101  # whatis

    def readScreen(self, observations):
        if parse(observations["tty_chars"][23])[:8] != "--More--":
            self.phase += 1
            if len(self.toName) >= 10 and not CONST_QUIET:
                print("Whoawhoawhoa, that's a lot of new monsters. (", end="")
                print(len(self.toName), end=")\n")
            return self.agenda[self.phase](self, observations)
        # turn = readTurn(observations)
        for x in range(len(observations["tty_chars"])):
            string = parse(observations["tty_chars"][x])
            open = string.find("<")
            if open == -1:
                continue
            close = string.find(">")
            if string[close+3] == "I":
                continue  # Don't bother trying to name something you can't see
            desc = string[close+6:]

            if desc.find("unknown creature causing you ") != -1:
                continue  # Don't bother trying to name paranoid delusions

            calledIndex = desc.find(" called ")

            needsName = False
            if calledIndex == -1:
                needsName = True
            else:
                name = desc[calledIndex+len(" called "):]
                end = name.find(" ")
                name = name[:end]
                if name[-1] == ",":
                    # snip commas off the end, they're not part of the name
                    name = name[:-1]
                try:
                    nameIndex = self.lookup[name]
                except KeyError:
                    needsName = True

            comma = string.find(",")
            col = int(string[open+1:comma])-1
            row = int(string[comma+1:close])

            if (row, col) == (readHeroPos(observations)):
                # No need to assign ourselves a database slot – 
                # we track our own condition quite closely already, tyvm.
                # You'd think we could just check if it has our name, but
                # it turns out sometimes the game gives a ghost our name.
                # We do want to name ghosts we see; so we'll detect the
                # "it's us" case this way instead.
                continue
            if observations["glyphs"][row][col] == 267:
                # We can't name shopkeepers.
                # Fortunately, they do actually have unique names already.
                i = -1
                for x in range(len(desc)):
                    if desc[x].isupper():
                        i = x
                        break
                if i == -1:
                    # FIXME: If this ever happens, fail more gracefully
                    print("Error code 6996: shopkeeper name handling", end="")
                    print(" in tracker.py failed miserably")
                    exit(1)
                name = desc[i:]
                commaIndex = name.find(",")
                if commaIndex != -1:
                    name = name[:commaIndex]
                else:
                    titleIndex = name.find(" the ")
                    if titleIndex != -1:
                        name = name[:titleIndex]
                    else:
                        end = name.find("  ")
                        name = name[:end]
                # We don't try-catch this like we did for the lookup before;
                # if we don't have an entry for this name we need to let the
                # exception fall through. We can't change a shopkeeper's name,
                # so the name had BETTER exist in our names already...
                nameIndex = self.lookup[name]
                needsName = False
            if observations["glyphs"][row][col] == 270:
                # We can't name The Oracle, but there's only one.
                nameIndex = self.lookup["The Oracle"]
                needsName = False
            if observations["glyphs"][row][col] == 271:
                # Aargh. It turns out aligned priests can't be named, but they
                # also aren't unique. I don't have a good solution for this,
                # but we have to do something, or else the agent will throw
                # every name it has at the priest and then panic. So, we'll
                # make the agent falsely believe there's only one aligned
                # priest. This comes with a couple downsides, but it'll
                # suffice for now, especially since it's unlikely the agent
                # will see more than one at a time.

                # Downside 1: If the agent statuses 1 aligned priest, it'll
                # think future aligned priests are statused.
                # Downside 2: When the agent sees a new priest, it'll forget
                # where it saw the previous priest.

                nameIndex = self.lookup["priest of"]
                needsName = False

            tameIndex = desc.find("tame")
            peaceIndex = desc.find("peaceful")
            stance = 1
            if peaceIndex != -1:
                stance = 0
            if tameIndex != -1:
                stance = -1

            if needsName:
                self.toName.append([row, col])
                self.stances.append(stance)
            else:
                self.database[nameIndex].updatePos([row, col], observations)
                self.database[nameIndex].hostility = stance
                self.visibleMonsters[row, col] = self.database[nameIndex]
        return 19  # next page, please

    def jotDownGlyphs(self, observations):
        for x in self.visibleMonsters:
            mon = self.visibleMonsters[x]
            row, col = mon.pos
            glyph = observations["glyphs"][row][col]
            mon.setGlyph(glyph)
        self.phase += 1
        return self.update(observations)

    def christenNewFaces(self, observations):
        if len(self.toName) == 0:
            return -1  # Naming complete, let's move on
        self.phase += 1
        # "What do you want to name?" -> A monster
        self.state.get("queue").append("m")
        return 27

    def moveCursor(self, observations):
        cursorPos = readCursorPos(observations)
        targetPos = self.toName[0]
        # Move cursor to the coordinates of targetPos
        if cursorPos[0] > targetPos[0] and cursorPos[1] > targetPos[1]:
            return 7
        if cursorPos[0] > targetPos[0] and cursorPos[1] < targetPos[1]:
            return 4
        if cursorPos[0] < targetPos[0] and cursorPos[1] > targetPos[1]:
            return 6
        if cursorPos[0] < targetPos[0] and cursorPos[1] < targetPos[1]:
            return 5
        if cursorPos[0] > targetPos[0]:
            return 0
        if cursorPos[0] < targetPos[0]:
            return 2
        if cursorPos[1] > targetPos[1]:
            return 3
        if cursorPos[1] < targetPos[1]:
            return 1
        # Cursor in correct place; input name
        name = self.getNewName()
        # There are occasions where you see a LOT of new monsters at once,
        # many far away. It's not totally ridiculous to imagine that naming
        # them might take 1000+ steps. So, we'll lax the 1000 step rule
        # countdown during the naming process. We can't be *too* lax with it
        # though, because the 10000 step rule is non-negotiatble.
        self.state.get("time").askForMoreTime(10)
        if name == None:
            panic = "Agent has panicked! (Reserve of monster names depleted.)"
            self.state.dumpCore(panic, observations)
            self.state.get("queue").append(65)
            self.state.get("queue").append(7)
            return 38
        self.database[self.lookup[name]].hostility = self.stances[0]
        self.database[self.lookup[name]].updatePos(targetPos, observations)
        glyph = observations["glyphs"][targetPos[0]][targetPos[1]]
        self.database[self.lookup[name]].setGlyph(glyph)
        monster = self.database[self.lookup[name]]
        self.visibleMonsters[targetPos[0], targetPos[1]] = monster
        name += "\n"  # Queue up an enter key press to confirm the name
        self.state.get("queue").append(name)
        self.phase -= 1
        self.toName = self.toName[1:]
        self.stances = self.stances[1:]
        return 18  # "." – select the thing on this square to name it

    def returnToTop(self):
        self.phase = 0
    agenda = [
        look,
        readScreen,
        jotDownGlyphs,
        christenNewFaces,
        moveCursor
    ]

    def getNewName(self):
        self.nextOpenName += 1
        if self.nextOpenName < len(monsterNames):
            return self.names[self.nextOpenName-1]
        else:
            # We could try to dip into the reserved names to survive, I guess
            # But I'd just as soon fail transparently
            return None

    def tattle(self, row, col):
        # Named for the skill in Paper Mario 64 and Paper Mario: The Thousand
        # Year Door; You point to a monster and ask for more information.
        # In this case, we fetch its database entry if possible.
        try:
            mon = self.visibleMonsters[row, col]
        except KeyError:
            # No database entry found.
            # Maybe whatever called this function pointed to a square with no
            # monster. Maybe the monster is something we can't log in the
            # database. Whatever the reason, we return None to signal "too bad,
            # no information available."
            return None
        else:
            return mon

    def annotate(self, string):
        # Takes a string, such as a message, and annotates it with monster
        # types of monster names. So, if ANNI is a giant ant, "ANNI" would be
        # replaced by "ANNI (giant ant)"
        # (Note: This is why names can't be substrings of each other)
        result = string
        for x in range(self.nextOpenName):
            name = self.names[x]
            pos = result.find(name)
            if pos == -1:
                continue
            insertionPoint = pos + len(name)
            mon = self.database[x].glyph
            mname = nh.permonst(nh.glyph_to_mon(mon)).mname
            desc = f' \x1b[0;36m({mname})\x1b[0;0m'
            result = result[:insertionPoint] + desc + result[insertionPoint:]
        return result


def scan(state, observations):
    action = state.get("tracker").update(observations)
    return action
