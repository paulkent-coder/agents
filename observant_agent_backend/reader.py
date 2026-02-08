#!/usr/bin/python

from .gamestate import StateModule
from .agent_config import *
from .utilities import *


class MessageSecretary(StateModule):
    def __init__(self, state):
        self.log = []
        self.state = state
        self.phase = 0
        self.lastKnownPos = [0, 0]

    def reset(self):
        if not CONST_QUIET:
            if len(self.log) == 0:
                # Should never happen, but just in case...
                print("Fate unclear. (No messages)")
            else:
                # The first message is usually race and role info.
                # Unfortunately, if the agent spawns on an item, or
                # if the game thinks it relevant to bring up the
                # phase of the moon (not kidding), then we don't
                # get that info.
                firstMsg = self.log[0][0]
                identityPos = firstMsg.find("You are a ")
                if identityPos == -1:
                    # emdash is a stylistic choice
                    print("Too bad – agent's identity was obscured.")
                else:
                    msg = firstMsg[identityPos+len("You are a "):]
                    print("Agent was a", msg)
                print("Recent messages:")
                # Print the last few messages logged before the agent died
                for string, streak in self.log[-3:]:
                    print("\t"+string, end="")
                    if streak > 1:
                        # If a message appears multiple times, that's a bad
                        # sign, so make it more visible in the logs.
                        print(" \x1b[0;33m("+str(streak)+"x)\x1b[0;0m")
                    else:
                        print("")

        self.log = []
        self.phase = 0

    def dumpCore(self):
        print("Recent messages:")
        # dumpCore is more detailed than reset; print 20 messages instead of 3
        for string, streak in self.log[-20:]:
            print("\t"+string, end="")
            if streak > 1:
                # If a message appears multiple times, that's a bad
                # sign, so make it more visible in the logs.
                print(" \x1b[0;33m("+str(streak)+"x)\x1b[0;0m")
            else:
                print("")

    def displayStats(self):
        pass

    def figureOutMessage(self, observations):
        message = readMessage(observations)	

        if message == "":
            # no message
            return -1

        if message[0] == "#":
            # agent inputting extended command; not worth logging
            return -1

        if message[-29:] == "(For instructions type a '?')":
            # not worth logging
            return -1

        if message[:24] == "What do you want to call":
            # not worth logging
            return -1

        if message == "There is nothing here to pick up.":
            # not worth logging
            return -1

        if message == "You see no objects here.":
            # not worth logging
            return -1

        if message == "It won't come off the hinges.":
            # not worth logging
            return -1

        if message == "The stairs are solidly fixed to the floor.":
            # not worth logging
            return -1

        if message == "There is nothing here to pick up.":
            # not worth logging
            return -1

        if message.find("This door is locked.") != -1:
            self.state.get("map").poke(observations, "locked")

        if message.find("You can't move diagonally into an intact doorway.") != -1:
            self.state.get("map").poke(observations, "baddoor")

        if message.find("You are carrying too much to get through.") != -1:
            self.state.get("map").poke(observations, "baddiag")

        if message.find("Your body is too large to fit through.") != -1:
            self.state.get("map").poke(observations, "baddiag")

        if message.find("You try to move the boulder, but in vain.") != -1:
            self.state.get("map").poke(observations, "badboulder")

        if message.find("You hear a monster behind the boulder.") != -1:
            self.state.get("map").poke(observations, "blockedboulder")

        if message.find("You cannot move the boulder.") != -1:
            self.state.get("map").poke(observations, "blockedboulder")

        if message.find("You read: \"") != -1:
            self.state.get("map").poke(observations, "engraving")

        # Situations where the agent is powerless to give names to monsters
        # tend to end badly, so we want to make sure we log them.
        if message.find("being called names") != -1:
            # Monster that refuses to take a name
            print(message)
        if message.find("You would never recognize") != -1:
            # Agent is hallucinating
            print(message)

        newPos = readHeroPos(observations)
        if newPos != self.lastKnownPos:
            # We're on a new square, so anything that was underfoot before
            # ain't underfoot now
            self.state.get("inventory").itemDetected("")
        self.lastKnownPos = newPos

        # TODO: Set the start and end of the message first,
        # then read the contents, so we don't need to repeat
        # the handling code for blind vs non-blind cases.
        if message.find("You see here ") != -1:
            # item underfoot
            start = message.find("You see here ") + len("You see here ")
            end = message.find(".", start)
            if end == -1:
                # FIXME: If this ever actually happens, a more graceful
                # recovery would be good.
                print("\x1b[0;31mFatal error: A \"you see here\"", end="")
                print(" message wasn't properly terminated...")
                print(message)
                exit(1)
            self.state.get("inventory").itemDetected(message[start:end])

        if message.find("You feel here ") != -1:
            # item underfoot (agent is blind)
            start = message.find("You feel here ") + len("You feel here ")
            end = message.find(".", start)
            if end == -1:
                # FIXME: If this ever actually happens, a more graceful
                # recovery would be good.
                print("\x1b[0;31mFatal error: A \"you feel here\"", end="")
                print(" message wasn't properly terminated...")
                print(message)
                exit(1)
            self.state.get("inventory").itemDetected(message[start:end])

        # For logging purposes, annotate the message
        # with the identities of any monsters mentioned in it.
        message = self.state.get("tracker").annotate(message)

        if observations["misc"][2]:
            # Vanilla Nethack prints "--More--" to the screen
            # when a message is too long. This --More-- isn't
            # included in the message string we read, so we
            # need to add it back in for logging purposes.
            message += " --More--"

        if len(self.log) > 0 and self.log[-1][0] == message:
            # Same message as last time; just increase the streak count
            self.log[-1][1] += 1
        else:
            self.log.append([message, 1])
        return -1

    def returnToTop(self):
        # Deprecated
        self.phase = 0


def read(state, observations):
    return state.get("reader").figureOutMessage(observations)
