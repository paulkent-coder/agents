#!/usr/bin/python

compass = {
	"N" : "k",
	"NE" : "u",
	"E" : "l",
	"SE" : "n",
	"S" : "j",
	"SW" : "b",
	"W" : "h",
	"NW" : "y"
}

keyLookup = {
	"a" : 97, 
	"b" : 98, 
	"c" : 99, 
	"d" : 100, 
	"e" : 101, 
	"f" : 102, 
	"g" : 103,
	"h" : 104,
	"i" : 105,
	"j" : 106,
	"k" : 107,
	"l" : 108,
	"m" : 109,
	"n" : 110,
	"o" : 111,
	"p" : 112,
	"q" : 113,
	"r" : 114,
	"s" : 115,
	"t" : 116,
	"u" : 117,
	"v" : 118,
	"w" : 119,
	"x" : 120,
	"y" : 121,
	"z" : 122, 
	"A" : 65, 
	"B" : 66, 
	"C" : 67, 
	"D" : 68, 
	"E" : 69, 
	"F" : 70, 
	"G" : 71,
	"H" : 72,
	"I" : 73,
	"J" : 74,
	"K" : 75,
	"L" : 76,
	"M" : 77,
	"N" : 78,
	"O" : 79,
	"P" : 80,
	"Q" : 81,
	"R" : 82,
	"S" : 83,
	"T" : 84,
	"U" : 85,
	"V" : 86,
	"W" : 87,
	"X" : 88,
	"Y" : 89,
	"Z" : 90,
	"." : 46,
	"," : 44,
	"<" : 60,
	">" : 62,
	";" : 59,
	"0" : 48,
	"1" : 49,
	"2" : 50,
	"3" : 51,
	"4" : 52,
	"5" : 53,
	"6" : 54,
	"7" : 55,
	"8" : 56,
	"9" : 57,
	"+" : 43,
	"-" : 45,
	" " : 32,
	"}" : 125, # represents enter ("}" serves no inherent purpose in nethack)
	"{" : -1 # special character; represents an open slot in the queue
}

#4) Command.KICK
#13) MiscAction.MORE
#15) Command.OVERVIEW
#16) UnsafeActions.PREVMSG
#18) Command.REDRAW
#20) Command.TELEPORT
#24) Command.ATTRIBUTES
#27) Command.ESC
#32) TextCharacters.SPACE
#33) Command.SHELL
#34) Command.SEEAMULET
#35) Command.EXTCMD
#36) Command.SEEGOLD
#38) Command.WHATDOES
#39) TextCharacters.APOS
#40) Command.SEETOOLS
#41) Command.SEEWEAPON
#42) Command.SEEALL
#43) Command.SEESPELLS
#44) Command.PICKUP
#45) TextCharacters.MINUS
#46) MiscDirection.WAIT
#47) Command.WHATIS
#48) TextCharacters.NUM_0
#49) TextCharacters.NUM_1
#50) TextCharacters.NUM_2
#51) TextCharacters.NUM_3
#52) TextCharacters.NUM_4
#53) TextCharacters.NUM_5
#54) TextCharacters.NUM_6
#55) TextCharacters.NUM_7
#56) TextCharacters.NUM_8
#57) TextCharacters.NUM_9
#58) Command.LOOK
#59) Command.GLANCE
#60) MiscDirection.UP
#61) Command.SEERINGS
#62) MiscDirection.DOWN
#63) UnsafeActions.HELP
#64) Command.AUTOPICKUP
#65) Command.TAKEOFFALL
#66) CompassDirectionLonger.SW
#67) Command.CALL
#68) Command.DROPTYPE
#69) Command.ENGRAVE
#70) Command.FIGHT
#71) Command.RUSH2
#72) CompassDirectionLonger.W
#73) Command.INVENTTYPE
#74) CompassDirectionLonger.S
#75) CompassDirectionLonger.N
#76) CompassDirectionLonger.E
#77) Command.MOVEFAR
#78) CompassDirectionLonger.SE
#79) Command.OPTIONS
#80) Command.PUTON
#81) Command.QUIVER
#82) Command.REMOVE
#83) Command.SAVE
#84) Command.TAKEOFF
#85) CompassDirectionLonger.NE
#86) Command.HISTORY
#87) Command.WEAR
#88) Command.TWOWEAPON
#89) CompassDirectionLonger.NW
#90) Command.CAST
#91) Command.SEEARMOR
#92) Command.KNOWN
#94) Command.SEETRAP
#95) Command.TRAVEL
#96) Command.KNOWNCLASS
#97) Command.APPLY
#98) CompassDirection.SW
#99) Command.CLOSE
#100) Command.DROP
#101) Command.EAT
#102) Command.FIRE
#103) Command.RUSH
#104) CompassDirection.W
#105) Command.INVENTORY
#106) CompassDirection.S
#107) CompassDirection.N
#108) CompassDirection.E
#109) Command.MOVE
#110) CompassDirection.SE
#111) Command.OPEN
#112) Command.PAY
#113) Command.QUAFF
#114) Command.READ
#115) Command.SEARCH
#116) Command.THROW
#117) CompassDirection.NE
#118) Command.VERSIONSHORT
#119) Command.WIELD
#120) Command.SWAP
#121) CompassDirection.NW
#122) Command.ZAP
#191) Command.EXTLIST
#193) Command.ANNOTATE
#195) Command.CONDUCT
#210) Command.RIDE
#212) Command.TIP
#225) Command.ADJUST
#227) Command.CHAT
#228) Command.DIP
#229) Command.ENHANCE
#230) Command.FORCE
#233) Command.INVOKE
#234) Command.JUMP
#236) Command.LOOT
#237) Command.MONSTER
#239) Command.OFFER
#240) Command.PRAY
#241) Command.QUIT
#242) Command.RUB
#243) Command.SIT
#244) Command.TURN
#245) Command.UNTRAP
#246) Command.VERSION
#247) Command.WIPE
