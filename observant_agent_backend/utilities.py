#!/usr/bin/python

# observant_agent

from .agent_config import *
from nle import nethack

keyLookup = {
    "a": 24,
    "b": 6,
    "c": 30,
    "d": 33,
    "e": 35,
    "f": 40,
    "g": 72,
    "h": 3,
    "i": 44,
    "j": 2,
    "k": 0,
    "l": 1,
    "m": 54,
    "n": 5,
    "o": 57,
    "p": 60,
    "q": 64,
    "r": 67,
    "s": 75,
    "t": 91,
    "u": 4,
    "v": 98,
    "w": 102,
    "x": 87,
    "y": 7,
    "z": 104,
    "A": 89,
    "B": 14,
    "C": 27,
    "D": 34,
    "E": 36,
    "F": 39,
    "G": 73,
    "H": 11,
    "I": 45,
    "J": 10,
    "K": 8,
    "L": 9,
    "M": 55,
    "N": 13,
    "O": 58,
    "P": 63,
    "Q": 66,
    "R": 69,
    "S": 74,
    "T": 88,
    "U": 12,
    "V": 43,
    "W": 99,
    "X": 95,
    "Y": 15,
    "Z": 28,
    ".": 18,
    ",": 61,
    "<": 16,
    ">": 17,
    ":": 51,
    "0": 110,
    "1": 111,
    "2": 112,
    "3": 113,
    "4": 114,
    "5": 115,
    "6": 116,
    "7": 117,
    "8": 118,
    "9": 119,
    "$": 120,
    "+": 105,
    "-": 106,
    " ": 107,
    "*": 76,
    "#": 20,
    # "?" : 21,
    "\n": 19  # represents enter
}


def parse(str):
    # The observations give us text in the form of ascii numbers
    # This turns those ascii numbers into something we can actually read
    return bytes(str).decode('ascii').replace('\0', '')


def readHeroPos(observations):
    # Returns hero row, hero col
    return observations["blstats"][1], observations["blstats"][0]


def readCursorPos(observations):
    # Returns cursor row, cursor col
    # (Relative to the game grid, not to the whole screen)
    return observations["tty_cursor"][0]-1, observations["tty_cursor"][1]


def readTurn(observations):
    return observations["blstats"][20]


def readMessage(observations):
    return parse(observations["message"])


def readDungeonNum(observations):
    return observations["blstats"][23]


def readDungeonLevel(observations):
    # Subtract one so it lines up with our zero-indexed arrays
    return observations["blstats"][24]-1


def iterableOverVicinity(observations=[], returnDirections=False, x=-1, y=-1):
    # There are several situations where we want to check the eight squares
    # surrounding us for some purpose or other.
    # This is a pain to do, and very susceptible to copy-paste errors.
    # So here it is in one canonical place.

    # This returns an iterable over the directions. Characteristics:
    # Type: Array
    # Shape: 8x2, with a couple exceptions:
    # if returnDirections is true, it's 8x3
    # some directions may be invalid if we're at map edge; if so, those
    # elements are None instead of an array
    # The first value in each pair is the row, and the second is the column
    # The third, if requested, is the string to feed to the last known
    # direction variable
    # Sorted by action number – array[#] is interacted with using action #

    output = []
    if observations != []:
        heroRow, heroCol = readHeroPos(observations)
    if x != -1:
        heroRow = x
    if y != -1:
        heroCol = y

    inconsistent = False
    if (x != -1) == (observations != []):
        inconsistent = True
    if (x != -1) != (y != -1):
        inconsistent = True
    if inconsistent and not CONST_QUIET:
        error = "Error code 666 – function \"iterableOverVicinity\""
        error += " requires either coordinates or observations to be passed "
        error += " in, but not both."

    if heroRow > 0:
        if returnDirections:
            output.append([heroRow-1, heroCol, "N"])
        else:
            output.append([heroRow-1, heroCol])
    else:
        output.append(None)

    if heroCol < 78:
        if returnDirections:
            output.append([heroRow, heroCol+1, "E"])
        else:
            output.append([heroRow, heroCol+1])
    else:
        output.append(None)

    if heroRow < 20:
        if returnDirections:
            output.append([heroRow+1, heroCol, "S"])
        else:
            output.append([heroRow+1, heroCol])
    else:
        output.append(None)

    if heroCol > 0:
        if returnDirections:
            output.append([heroRow, heroCol-1, "W"])
        else:
            output.append([heroRow, heroCol-1])
    else:
        output.append(None)

    if heroRow > 0 and heroCol < 78:
        if returnDirections:
            output.append([heroRow-1, heroCol+1, "NE"])
        else:
            output.append([heroRow-1, heroCol+1])
    else:
        output.append(None)

    if heroRow < 20 and heroCol < 78:
        if returnDirections:
            output.append([heroRow+1, heroCol+1, "SE"])
        else:
            output.append([heroRow+1, heroCol+1])
    else:
        output.append(None)

    if heroRow < 20 and heroCol > 0:
        if returnDirections:
            output.append([heroRow+1, heroCol-1, "SW"])
        else:
            output.append([heroRow+1, heroCol-1])
    else:
        output.append(None)

    if heroRow > 0 and heroCol > 0:
        if returnDirections:
            output.append([heroRow-1, heroCol-1, "NW"])
        else:
            output.append([heroRow-1, heroCol-1])
    else:
        output.append(None)

    return output


def readHeroStatus(observations, statusToCheck):
    # Checks if the hero is afflicted with a specific status condition,
    # indicated by number
    # Options are:
    # (0) Petrification
    # (1) Degeneration into slime
    # (2) Strangulation
    # (3) Food poisoning
    # (4) Disease
    # (5) Blindness
    # (6) Deafness
    # (7) Stunning
    # (8) Confusion
    # (9) Hallucination
    # (10) Levitation
    # (11) Flight
    # (12) Riding
    condition = observations["blstats"][nethack.NLE_BL_CONDITION]
    status = [
        bool(condition & nethack.BL_MASK_STONE),
        bool(condition & nethack.BL_MASK_SLIME),
        bool(condition & nethack.BL_MASK_STRNGL),
        bool(condition & nethack.BL_MASK_FOODPOIS),
        bool(condition & nethack.BL_MASK_TERMILL),
        bool(condition & nethack.BL_MASK_BLIND),
        bool(condition & nethack.BL_MASK_DEAF),
        bool(condition & nethack.BL_MASK_STUN),
        bool(condition & nethack.BL_MASK_CONF),
        bool(condition & nethack.BL_MASK_HALLU),
        bool(condition & nethack.BL_MASK_LEV),
        bool(condition & nethack.BL_MASK_FLY),
        bool(condition & nethack.BL_MASK_RIDE)
    ]
    return status[statusToCheck]


def readInventoryGlyph(state, observations, index):
    # TODO: Account for hallucination.
    # While the agent is hallucinating, the glyphs in its inventory
    # are distorted, but the string descriptions are reliable.
    # Thus, while we're hallucinating, we should read the string
    # and infer what the glyph is from that. This is annoying, and
    # hallucination is uncommon, so this is on the backburner for now.
    return observations["inv_glyphs"][index]


def readInventoryStrs(state, observations, index):
    return parse(observations["inv_strs"][index])


def printScreen(observations):
    print("")
    for x in range(len(observations["tty_chars"])):
        print(parse(observations["tty_chars"][x]))
    print("")


def readHeroHealth(observations):
    hp = observations["blstats"][nethack.NLE_BL_HP]
    max = observations["blstats"][nethack.NLE_BL_HPMAX]
    return hp, max
