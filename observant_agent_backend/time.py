#!/usr/bin/python

from .gamestate import StateModule
from .utilities import *
import time

class Stopwatch(StateModule):
	agenda = []
	def __init__(self, state):
		self.startTime = time.clock_gettime(time.CLOCK_UPTIME_RAW)
		self.lastKnownTurn = 1
		self.stepsThisTurn = 0
		self.state = state
		self.alreadyPanicked = False		
		self.stats_runs = 0
		self.stats_steps = 0
		self.stats_turns = 0
		self.stats_speed = 0
	def reset(self):
		currTime = time.clock_gettime(time.CLOCK_UPTIME_RAW)
		Hz = self.lastKnownTurn / (currTime - self.startTime)
		if not CONST_QUIET:
			print(self.lastKnownTurn,"turns taken at",Hz,"Hz.")
		
		self.stats_runs += 1
		self.stats_turns += self.lastKnownTurn
		self.stats_speed += Hz
		
		self.startTime = currTime
		self.lastKnownTurn = 1
		self.stepsThisTurn = 0
		self.alreadyPanicked = False
		if self.stepsThisTurn >= 1000:
			print(self.stepsThisTurn,"steps taken this turn.")
	def dumpCore(self):
		pass
	def displayStats(self):
		print("Average steps per run:",(self.stats_steps/self.stats_runs))
		print("Average turns per run:",(self.stats_turns/self.stats_runs))
		print("Average steps per turn:",(self.stats_steps/self.stats_turns))
		print("Average processing speed:",(self.stats_speed/self.stats_runs),"Hz")

	def updateTurns(self, turns):
		if self.lastKnownTurn != turns:
			self.stepsThisTurn = 0
		self.lastKnownTurn = turns
	def incrementTurns(self):
		self.lastKnownTurn += 1
		self.stepsThisTurn = 0
	def nextStep(self,observations):
		self.stepsThisTurn += 1
		self.stats_steps += 1
		if self.stepsThisTurn >= 900:
			x = 1
		if self.stepsThisTurn >= 1000 and not self.alreadyPanicked:
			# If *this* many steps happened without any time passing, it's a fair bet we're stuck.
			# So, rather than wait to get slaughtered by the 10000 step rule, let's dump core and quit.
			self.state.dumpCore("Agent has panicked! (1000 steps passed planning for one turn.)",observations)
			self.state.get("queue").cutInLine(7)
			self.state.get("queue").cutInLine(65)
			self.state.get("queue").cutInLine(38)
			self.alreadyPanicked = True
			return 38 # Escape out of whatever we were doing, quit, and then next step, answer yes to "are you sure?"
				# (We have to hit escape twice to be sure. If we're halfway through a naming prompt,
				# pressing escape once merely clears the prompt, and then the 65 press prints an illegible character to screen,
				# which causes the entire program to die. Not what we want.)
		return -1
	def askForMoreTime(self, amount):
		# Forestalls the 1000-rule panic.
		self.stepsThisTurn -= amount

def countStep(state, observations):
	return state.get("time").nextStep(observations)