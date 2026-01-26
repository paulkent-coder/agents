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
				print("Fate unclear. (No messages)")
			else:
				firstMsg = self.log[0][0]
				identityPos = firstMsg.find("You are a ")
				if identityPos == -1:
					print("Too bad – agent's identity was obscured.")
				else:
					print("Agent was a",firstMsg[identityPos+len("You are a "):])
				print("Recent messages:")
				for string, streak in self.log[-3:]:
					if streak > 1:
						print("\t"+string+" \x1b[0;33m("+str(streak)+"x)\x1b[0;0m")
					else: 
						print("\t"+string)
		self.log = []
		self.phase = 0
	def dumpCore(self):
		print("Recent messages:")
		for string, streak in self.log[-20:]:
			if streak > 1:
				print("\t"+string+" \x1b[0;33m("+str(streak)+"x)\x1b[0;0m")
			else: 
				print("\t"+string)
				
	def displayStats(self):
		pass
	def figureOutMessage(self,observations):
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
			
		if message.find("being called names") != -1:
			print(message)
		if message.find("You would never recognize") != -1:
			print(message)
		
		newPos = readHeroPos(observations)
		if newPos != self.lastKnownPos:
			# We're on a new square, so anything that was underfoot before ain't underfoot anymore
			self.state.get("inventory").itemDetected("")
		self.lastKnownPos = newPos
		
		if message.find("You see here ") != -1:
			# item underfoot
			start = message.find("You see here ") + len("You see here ")
			end = message.find(".",start)
			if(end == -1):
				print("\x1b[0;31mFatal error: A \"you see here\" message wasn't properly terminated...")
				print(message)
				exit(1)
			self.state.get("inventory").itemDetected(message[start:end])
		
		if message.find("You feel here ") != -1:
			# item underfoot
			start = message.find("You feel here ") + len("You feel here ")
			end = message.find(".",start)
			if(end == -1):
				print("\x1b[0;31mFatal error: A \"you feel here\" message wasn't properly terminated...")
				print(message)
				exit(1)
			self.state.get("inventory").itemDetected(message[start:end])
			
			
		message = self.state.get("tracker").annotate(message)
		
		if observations["misc"][2]:
			message += " --More--"
		
		if len(self.log) > 0 and self.log[-1][0] == message:
			self.log[-1][1] += 1
		else:
			self.log.append([message,1])
		return -1
	
	def returnToTop(self):
		# Deprecated
		self.phase = 0

def read(state, observations):
	return state.get("reader").figureOutMessage(observations)