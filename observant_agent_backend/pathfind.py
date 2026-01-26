#!/usr/bin/python

# So, let me brainstorm some pathfinding routines I might want
# NOTE: All of the functions in this file operate under the assumption that #Terrain is active

from .utilities import *
from .agent_config import *

# Fix-up
# Repair an existing route, by aiming for any of the spaces left on the viable route,
# and then append the rest of the route we were following before to the "return to route" route

def pathfindFixUp(gazetteer, observations, prevActions, prevRoute):
	# GOAL: Get to any of the coordinate pairs en route
	# Returns a list of actions and a list of coordinates (in that order)
	heroRow, heroCol = readHeroPos(observations)
	try:
		index = prevRoute.index([heroRow,heroCol])
	except ValueError:
		pass
	else:
		# We're actually still on the path. We just skipped ahead.
		# So, we delete some of the front of the movement queue and call it a day.
		return prevActions[index:], prevRoute[index:]
	
	investigated = [([False] * 79)]
	route = [([None] * 79)]
	actions = [([None] * 79)]
	distance = [([0] * 79)]
	for x in range(20):
		# I'd love to multiply all these arrays by 20 but that gives us shallow copies of their rows
		# so we gotta do this the slightly clumsier way
		investigated.append(investigated[0].copy())
		route.append(route[0].copy())
		actions.append(actions[0].copy())
		distance.append(distance[0].copy())
	queue = [[heroRow,heroCol]]
	
	route[heroRow][heroCol] = [[heroRow, heroCol]]
	actions[heroRow][heroCol] = []
	
	while len(queue) > 0:
		row, col = queue[0]
		queue = queue[1:] # pop the element at the front of the queue since we're looking at it now
		if investigated[row][col]: # don't investigate the same space twice, that's inefficient
			continue # if this path was faster we'd have investigated it before the other path
		if distance[row][col] > CONST_MAX_ROUTE_REPAIR_DIST:
			# Repairing the route is taking too long. Let's just make a new one
			return None, None
		investigated[row][col] = True
		dirs = iterableOverVicinity(x=row,y=col)
		for x in range(8): 
			if dirs[x] == None:
				continue # out of bounds
			r, c = dirs[x]
			if gazetteer.isMovementPossible(observations,[row,col],[r,c]):
				try:
					index = prevRoute.index([r,c])
				except ValueError:
					if actions[r][c] == None:
						queue.append([r,c])
						distance[r][c] = distance[row][col] + 1
						actions[r][c] = actions[row][col] + [x]
						route[r][c] = route[row][col] + [[r,c]]
				else:
					# Aha, back on track.
					finalActions = actions[row][col] + [x] + prevActions[index:]
					finalRoute = route[row][col] + prevRoute[index:]
					return finalActions, finalRoute
	return None, None

# A*
# Efficiently draw up a route to a specific pair of coordinates using A*

def pathfindAStar(gazetteer, observations, target, start=[]):
	# TODO
	pass

# Djistrika's
# Examine the surrounding spaces until you see a square that looks like it's worth going for

def forwardWeGo(gazetteer, observations):
	# GOAL: Find the stairs or unexplored turf
	# Returns a list of actions and a list of coordinates (in that order)
	heroRow, heroCol = readHeroPos(observations)
	if gazetteer.readSquare(observations,heroRow,heroCol) == 2383:
		# we're... we're already there tho...
		return [], []
	
	investigated = [([False] * 79)]
	route = [([None] * 79)]
	actions = [([None] * 79)]
	distance = [([0] * 79)]
	for x in range(20):
		# I'd love to multiply all these arrays by 20 but that gives us shallow copies of their rows
		# so we gotta do this the slightly clumsier way
		investigated.append(investigated[0].copy())
		route.append(route[0].copy())
		actions.append(actions[0].copy())
		distance.append(distance[0].copy())
	queue = [[heroRow,heroCol]]
	
	route[heroRow][heroCol] = [[heroRow,heroCol]]
	actions[heroRow][heroCol] = []
	
	while len(queue) > 0:
		row, col = queue[0]
		queue = queue[1:] # pop the element at the front of the queue since we're looking at it now
		if investigated[row][col]: # don't investigate the same space twice, that's inefficient
			continue # if this path was faster we'd have investigated it before the other path
	
		investigated[row][col] = True
		dirs = iterableOverVicinity(x=row,y=col)
		for x in range(8): 
			if dirs[x] == None:
				continue # out of bounds
			r, c = dirs[x]
			if gazetteer.readSquare(observations,r,c) == 2359:
				# We don't want to route all the way to the unknown square, it could be hazardous
				# Going to the last known space before the unknown one will reveal it, then we can plan from there
				return actions[row][col], route[row][col]
			if gazetteer.isMovementPossible(observations,[row,col],[r,c]):
				if actions[r][c] == None:
					queue.append([r,c])
					distance[r][c] = distance[row][col] + 1
					actions[r][c] = actions[row][col] + [x]
					route[r][c] = route[row][col] + [[r,c]]
				if gazetteer.readSquare(observations,r,c) == 2383:
					return actions[r][c], route[r][c]
	gazetteer.modeSwitch("dsp") # We're out of obvious paths. Time to start searching for secret doors
	return gropeForDoors(gazetteer, observations)
	
	
# TODO: More policies might be nice

# Desperation
# Move to the nearest square that we haven't yet searched to exhaustion,
# with the caveat that squares that aren't adjacent to walls don't qualify

def gropeForDoors(gazetteer, observations):
	# GOAL: Find the stairs or unexplored turf nearby, or failing that a wall to search
	# Returns a list of actions and a list of coordinates (in that order)
	heroRow, heroCol = readHeroPos(observations)
	if gazetteer.readSquare(observations,heroRow,heroCol) == 2383:
		# we're... we're already there tho...
		return [], []
	
	investigated = [([False] * 79)]
	route = [([None] * 79)]
	actions = [([None] * 79)]
	distance = [([0] * 79)]
	for x in range(20):
		# I'd love to multiply all these arrays by 20 but that gives us shallow copies of their rows
		# so we gotta do this the slightly clumsier way
		investigated.append(investigated[0].copy())
		route.append(route[0].copy())
		actions.append(actions[0].copy())
		distance.append(distance[0].copy())
	queue = [[heroRow,heroCol]]
	
	route[heroRow][heroCol] = [[heroRow,heroCol]]
	actions[heroRow][heroCol] = []
	
	bestRouteSoFar = None
	bestActionsSoFar = None
	bestCostSoFar = None
	
	currSquareCost = determineSearchCost(gazetteer, observations, heroRow, heroCol)
	if currSquareCost != None:
		bestCostSoFar = currSquareCost - CONST_SEARCH_DEPTH_BIAS
		bestRouteSoFar = [[heroRow,heroCol]]
		bestActionsSoFar = []
	
	while len(queue) > 0:
		row, col = queue[0]
		queue = queue[1:] # pop the element at the front of the queue since we're looking at it now
		if investigated[row][col]: # don't investigate the same space twice, that's inefficient
			continue # if this path was faster we'd have investigated it before the other path
		if (distance[row][col] > CONST_MAX_GROPE_DIST) and (bestCostSoFar != None):
			# Aight, we've checked the area, let's decide what to do.
			# (If we somehow haven't found any walls yet, we keep looking for one.)
			break
		investigated[row][col] = True
		dirs = iterableOverVicinity(x=row,y=col)
		currSquareCost = determineSearchCost(gazetteer, observations, row, col)
		if currSquareCost != None:
			currSquareCost += distance[row][col]
			if bestCostSoFar == None or currSquareCost < bestCostSoFar:
				bestCostSoFar = currSquareCost
				bestRouteSoFar = route[row][col]
				bestActionsSoFar = actions[row][col]
		for x in range(8): 
			if dirs[x] == None:
				continue # out of bounds
			r, c = dirs[x]
			if gazetteer.readSquare(observations,r,c) == 2374 or gazetteer.readSquare(observations,r,c) == 2375:
				if x < 4 and gazetteer.hasTagObs("locked", r, c, observations):
					# Alright, we've got a locked door here.
					# We might have to kick it down.
					# This is a bit risky so we'll give the action a cost of CONST_KICK_DOOR_COST
					# But does it actually lead anywhere new? If not there's no point
					doordirs = iterableOverVicinity(x=r, y=c)
					somewhereNew = False
					for y in range(8):
						if dirs[y] == None:
							continue # out of bounds
						if gazetteer.readSquare(observations,doordirs[y][0], doordirs[y][1]) == 2359:
							somewhereNew = True
							if somewhereNew:
								# Evidently, yes, yes it does lead somewhere new.
								# So – is it worth it?
								doorCost = distance[row][col] + CONST_KICK_DOOR_COST
								if doorCost < bestCostSoFar:
									bestCostSoFar = doorCost
									bestRouteSoFar = route[row][col] + [[row, col]]
									bestActionsSoFar = actions[row][col] + [[48, x]]
			if gazetteer.readSquare(observations,r,c) == 2359:
				# Ooooooh! Unexplored turf! Let's get going!
				gazetteer.modeSwitch("std")
				return actions[row][col], route[row][col]
			if gazetteer.isMovementPossible(observations,[row,col],[r,c]):
				if actions[r][c] == None:
					queue.append([r,c])
					distance[r][c] = distance[row][col] + 1
					actions[r][c] = actions[row][col] + [x]
					route[r][c] = route[row][col] + [[r,c]]
				if gazetteer.readSquare(observations,r,c) == 2383:
					# Ooooooh! The stairs! Let's get going!
					gazetteer.modeSwitch("std")
					return actions[r][c], route[r][c]
	# pick something
	searchArray = [75] * (CONST_SEARCH_DEPTH_BIAS + 2)
	stayInPlaceArray = [bestRouteSoFar[-1]] * (CONST_SEARCH_DEPTH_BIAS + 2)
	return bestActionsSoFar + searchArray, bestRouteSoFar + stayInPlaceArray
	

def determineSearchCost(gazetteer,observations,row,col):
	leastExploredWall = None
	dirs = iterableOverVicinity(x=row,y=col)
	wallsAround = 0
	for x in range(8): 
		if dirs[x] == None:
			continue # out of bounds
		r, c = dirs[x]
		glyph = gazetteer.readSquare(observations,r,c)
		if glyph >= 2360 and glyph <= 2370:
			wallsAround += 1
			wallCost = gazetteer.readSearchMap(r,c,observations)
			if leastExploredWall == None or wallCost < leastExploredWall:
				leastExploredWall = wallCost
	if leastExploredWall != None:
		if gazetteer.isSearchHotspot(observations):
			leastExploredWall -= CONST_SEARCH_HOTSPOT_BIAS
		leastExploredWall -= CONST_SEARCH_MULTIWALL_BIAS * wallsAround
	return leastExploredWall