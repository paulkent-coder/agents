#!/usr/bin/env python3
import nle
import gym
import aicrowd_gym
from nle import nethack as nh

# If wizard mode isn't working: go to the nle library, open env/tasks.py, and comment out line 331

keyLookup = {
	"a" : 24,
	"b" : 6,
	"c" : 30,
	"d" : 33,
	"e" : 35,
	"f" : 40,
	"g" : 72,
	"h" : 3,
	"i" : 44,
	"j" : 2,
	"k" : 0,
	"l" : 1,
	"m" : 54,
	"n" : 5,
	"o" : 57,
	"p" : 60,
	"q" : 64,
	"r" : 67,
	"s" : 75,
	"t" : 91,
	"u" : 4,
	"v" : 98,
	"w" : 102,
	"x" : 87,
	"y" : 7,
	"z" : 104,
	"A" : 89,
	"B" : 14,
	"C" : 27,
	"D" : 34,
	"E" : 36,
	"F" : 39,
	"G" : 73,
	"H" : 11,
	"I" : 45,
	"J" : 10,
	"K" : 8,
	"L" : 9,
	"M" : 55,
	"N" : 13,
	"O" : 58,
	"P" : 63,
	"Q" : 66,
	"R" : 69,
	"S" : 74,
	"T" : 88,
	"U" : 12,
	"V" : 43,
	"W" : 99,
	"X" : 95,
	"Y" : 15,
	"Z" : 28,
	"." : 18,
	"," : 61,
	"<" : 16,
	">" : 17,
	":" : 51,
	"0" : 110,
	"1" : 111,
	"2" : 112,
	"3" : 113,
	"4" : 114,
	"5" : 115,
	"6" : 116,
	"7" : 117,
	"8" : 118,
	"9" : 119,
	"$" : 120,
	"+" : 105,
	"-" : 106,
	" " : 107,
	"*" : 76,
	"#" : 20,
	# "?" : 21,
	"~" : 19, # represents enter
	"\\" : 38 # represents escape
}

def parse(str):
	# The observations give us text in the form of ascii numbers
	# This turns those ascii numbers into something we can actually read
	return bytes(str).decode('ascii').replace('\0','')

env = aicrowd_gym.make("NetHackChallenge-v0", character="tou", wizard=True, savedir=None)  # (Don't save a recording of the episode)

sequence = "#wizlevelport~10~"

for x in range(1000):
	print(x)
	env.reset()
	for y in sequence:
		env.step(keyLookup[y])
	
exit(0)

obs = env.reset()  # each reset generates a new dungeon
while True:
	env.render()
	action = input("Next action? ")
	for x in action:
		env.step(keyLookup[x])