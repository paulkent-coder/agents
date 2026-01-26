#!/usr/bin/env python3
import nle
import gym
import aicrowd_gym

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
	"~" : 19, # represents enter
	"\\" : 38 # represents escape
}

env = aicrowd_gym.make("NetHackChallenge-v0", wizard=True, savedir=None)

sequence = "#wizlevelport~10~"

for x in range(1000):
	env.reset()
	for y in sequence:
		env.step(keyLookup[y])