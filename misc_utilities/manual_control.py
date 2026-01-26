import numpy as np
from .keyLookup import *
from .items import *

from agents.base import BatchedAgent


# Here's a compass, just for reference...
# y k u
#  \|/
# h-.-l
#  /|\
# b j n

def parse(str):
    # The observations give us text in the form of ascii numbers
    # This turns those ascii numbers into something a bit more immediately legible
    return bytes(str).decode('ascii').replace('\0','')

def readMessage(observations):
    return parse(observations["message"])

def readHeroPos(observations):
    # Returns hero row, hero col
    return observations["blstats"][1], observations["blstats"][0]

class ManualControl(BatchedAgent):
    def __init__(self, num_envs, num_actions):
        pass
        
    def batched_step(self, observations, rewards, dones, infos):
        """
        Perform a batched step on lists of environment outputs.

        Each argument is a list of the respective gym output.
        Returns an iterable of actions.
        """    
        actions = []
        for x in range(len(dones)):
            print("MESSAGE: " + readMessage(observations[x]))
            heroY, heroX = readHeroPos(observations[x])
            print("HERO COORDINATES: (" + str(heroX) + ", " + str(heroY) + ")")
            nextAction = int(input())
            actions.append(nextAction)
        return actions