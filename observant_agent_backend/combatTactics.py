#!/usr/bin/python

def isWorthFighting(state, observations, monster):
	hostility = monster.hostility
	glyph = monster.glyph
	
	# TODO: Add more logic! :D
	
	if hostility != 1:
		# Maybe later we'll consider being mean to peacefuls
		# But in any case we definitely don't want to be mean to pets
		return False
	
	if glyph == 27 and observations["blstats"][10] < 21:
		# Oh boy, a gas spore. Yikes.
		# At 21 HP, a gas spore explosion has a 2.7% chance to kill us, which I'm willing to put up with.
		# If our HP is any lower than that, let's not take the risk.
		return False
	
	if glyph == 28:
		# Hitting a floating eye is asking for trouble.
		# TODO: Check if we're blind, because if we're blind we're fine to hit it.
		return False
	
	if (glyph >= 156 and glyph <= 159) or glyph == 55 or glyph == 56:
		# The molds are sessile and have painful passive counterattacks, so don't antagonize them
		return False
	
	return True

def meleeCombat(state, observations):
	from .utilities import iterableOverVicinity
	dirs = iterableOverVicinity(observations)
	for direction in range(len(dirs)):
		if dirs[direction] == None:
			# out of bounds
			continue
		row, col = dirs[direction]
		monster = state.get("tracker").tattle(row,col)
		if monster == None:
			continue
		if isWorthFighting(state, observations, monster):
			state.get("queue").append(direction)
			return 39 # fight
	return -1