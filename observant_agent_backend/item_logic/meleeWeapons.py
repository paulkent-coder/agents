#!/usr/bin/env python3

# TODO

# The value of a weapon is determined by the following:
	# The to-hit bonus of the weapon (higher = more value)
	# The damage output of the weapon (higher = more value)
	# The agent's current skill level with that weapon type (higher = more value)
	# The agent's maximum skill level with that weapon type (higher = more value)
	# The viability of that weapon's skill (more viability = more value)
		# example: sling proficiency is worthless late game, so high max sling skill isn't worth much
	# Whether the weapon is silver (yes = more value... unless the agent has been afflicted with silver-hating)
	# Whether the weapon is cursed (yes = less value)
		# (a weapon being cursed should apply a flat penalty to total value.)
		# (if an weapon is super strong on its own merit, we might wield it despite the curse.)
	# Whether we already have a better weapon for that slot (yes = less value)
	# Whether the agent is a monk (yes = less value)

#def calcWeaponSmallDamage(itemString):
#	baseDamage = baseWeaponDamageVSSmall(itemString) + readWeaponEnchantment(itemString)

def readWeaponEnchantment(itemString):
	for x in range(len(itemString)-1):
		sign = itemString[x]
		if sign != "+" and sign != "-":
			continue
		if not itemString[x+1].isdigit():
			continue
		y = x
		number = ""
		while y < len(itemString):
			if not itemString[y].isdigit():
				if sign == "-":
					return -1 * int(number)
				else:
					return int(number)
			number += itemString[y]
			y += 1
	return None

def baseWeaponDamageVSSmall(itemString):
	# Daggers
	if itemString.find("orcish dagger") != -1 or itemString.find("crude dagger") != -1:
		return 2
	if itemString.find("silver dagger") != -1:
		return 2.5
	if itemString.find("elven dagger") != -1 or itemString.find("runed dagger") != -1:
		return 3
	if itemString.find("dagger") != -1:
		return 2.5
	if itemString.find("athame") != -1:
		return 2.5
	# Knives
	if itemString.find("worm tooth") != -1 or itemString.find("worm teeth") != -1:
		return 1.5
	if itemString.find("crysknife") != -1 or itemString.find("crysknives") != -1:
		return 5.5
	if itemString.find("knife") != -1 or itemString.find("knives") != -1 or itemString.find("shito") != -1:
		return 2
	if itemString.find("stiletto") != -1:
		return 2
	if itemString.find("scalpel") != -1:
		return 2
	# Pick-axes
	if itemString.find("pick-axe") != -1:
		return 3.5
	if itemString.find("dwarvish mattock") != -1 or itemString.find("broad pick"):
		return 6.5
	# Short swords
	if itemString.find("orcish short sword") != -1 or itemString.find("crude short sword") != -1:
		return 3
	if itemString.find("dwarvish short sword") != -1 or itemString.find("broad short sword") != -1:
		return 4
	if itemString.find("elven short sword") != -1 or itemString.find("runed short sword") != -1:
		return 4.5
	if itemString.find("short sword") != -1 or itemString.find("wakizashi") != -1:
		return 3.5
	# Broadswords
	# NOTE: "runed broadswords" can refer to either runeswords or elven broadswords,
	# but since runeswords other than Stormbringer can only be found by wishing,
	# we'll just assume arbitrary runed broadswords are elven broadswords.
	if itemString.find("runed broadsword") != -1 or itemString.find("elven broadsword") != -1:
		return 6
	if itemString.find("runesword") != -1:
		return 5
	if itemString.find("broadsword") != -1 or itemString.find("ninja-to") != -1:
		return 5
	# Long swords
	if itemString.find("long sword") != -1:
		return 4.5
	if itemString.find("katana") != -1 or itemString.find("samurai sword") != -1:
		return 5.5
	# Two-handed swords
	if itemString.find("two-handed sword") != -1:
		return 6.5
	if itemString.find("tsurugi") != -1 or itemString.find("long samurai sword") != -1:
		return 8.5
	# Scimitars
	if itemString.find("scimitar") != -1 or itemString.find("curved sword") != -1:
		return 4.5
	# Sabers
	if itemString.find("silver saber") != -1:
		return 4.5
	# Clubs
	if itemString.find("aklys") != -1 or itemString.find("thonged club") != -1:
		return 3.5
	if itemString.find("club") != -1:
		return 3.5
	# Maces
	if itemString.find("mace") != -1:
		return 4.5
	# Morning stars
	if itemString.find("morning star") != -1:
		return 5
	# Flails
	if itemString.find("flail") != -1 or itemString.find("nunchaku") != -1:
		return 4.5
	if itemString.find("grappling hook") != -1 or itemString.find("iron hook") != -1:
		return 1.5
	# Hammers
	if itemString.find("war hammer") != -1:
		return 3.5
	# Staves
	if itemString.find("staff") != -1 or itemString.find("staves") != -1:
		return 3.5
	# Polearms
	if itemString.find("partisan") != -1 or itemString.find("vulgar polearm") != -1:
		return 3.5
	if itemString.find("fauchard") != -1 or itemString.find("pole sickle") != -1:
		return 3.5
	if itemString.find("glaive") != -1 or itemString.find("naginata") != -1 or itemString.find("single-edged polearm") != -1:
		return 3.5
	if itemString.find("bec-de-corbin") != -1 or itemString.find("beaked polearm") != -1:
		return 4.5
	if itemString.find("spetum") != -1 or itemString.find("forked polearm") != -1:
		return 4.5
	if itemString.find("lucern hammer") != -1 or itemString.find("pronged polearm") != -1:
		return 5
	if itemString.find("bill-guisarme") != -1 or itemString.find("hooked polearm") != -1:
		return 5
	if itemString.find("guisarme") != -1 or itemString.find("pruning hook") != -1:
		return 5
	if itemString.find("ranseur") != -1 or itemString.find("hilted polearm") != -1:
		return 5
	if itemString.find("voulge") != -1 or itemString.find("pole cleaver") != -1:
		return 5
	if itemString.find("bardiche") != -1 or itemString.find("long poleaxe") != -1:
		return 5
	if itemString.find("halberd") != -1 or itemString.find("angled poleaxe") != -1:
		return 5.5
	# Axes
	if itemString.find("battle-axe") != -1:
		return 7
	if itemString.find("axe") != -1:
		return 3.5
	# Spears
	if itemString.find("orcish spear") != -1 or itemString.find("crude spear") != -1:
		return 3
	if itemString.find("elven spear") != -1 or itemString.find("runed spear") != -1:
		return 4
	if itemString.find("dwarven spear") != -1 or itemString.find("stout spear") != -1:
		return 4.5
	if itemString.find("javelin") != -1 or itemString.find("throwing spear") != -1:
		return 3.5
	if itemString.find("silver spear") != -1:
		return 3.5
	if itemString.find("spear") != -1:
		return 3.5
	# Tridents
	if itemString.find("trident") != -1:
		return 4.5
	# Lances
	if itemString.find("lance") != -1:
		return 3.5
	# Crossbow
	if itemString.find("crossbow bolt") != -1:
		return 3.5
	if itemString.find("crossbow") != -1:
		return 1.5
	# Archery
	if itemString.find("orcish bow") != -1 or itemString.find("crude bow") != -1:
		return 1.5
	if itemString.find("orcish arrow") != -1 or itemString.find("crude arrow") != -1:
		return 3
	if itemString.find("elven bow") != -1 or itemString.find("runed bow") != -1:
		return 1.5
	if itemString.find("elven arrow") != -1 or itemString.find("runed arrow") != -1:
		return 4
	if itemString.find("yumi") != -1 or itemString.find("long bow") != -1:
		return 1.5
	if itemString.find("ya") != -1 or itemString.find("bamboo arrow") != -1:
		return 4
	if itemString.find("silver arrow") != -1:
		return 3.5
	if itemString.find("bow") != -1:
		return 1.5
	if itemString.find("arrow") != -1:
		return 3.5
	# Sling
	if itemString.find("sling") != -1:
		return 1.5
	if itemString.find("flint stone") != -1:
		return 3.5
	# Dart
	if itemString.find("dart") != -1:
		return 2
	# Shuriken
	if itemString.find("shuriken") != -1 or itemString.find("throwing star"):
		return 4.5
	# Boomerang
	if itemString.find("boomerang") != -1:
		return 5
	# Whip
	if itemString.find("whip") != -1:
		return 1.5
	if itemString.find("rubber hose") != -1:
		return 2.5
	# Unicorn Horn
	if itemString.find("unicorn horn") != -1:
		return 6.5
	# TODO: Recognize artifacts
	return -999 # not a weapon

def baseWeaponDamageVSLarge(itemString):
	# Daggers
	if itemString.find("orcish dagger") != -1 or itemString.find("crude dagger") != -1:
		return 2
	if itemString.find("silver dagger") != -1:
		return 2
	if itemString.find("elven dagger") != -1 or itemString.find("runed dagger") != -1:
		return 2
	if itemString.find("dagger") != -1:
		return 2
	if itemString.find("athame") != -1:
		return 2
	# Knives
	if itemString.find("worm tooth") != -1 or itemString.find("worm teeth") != -1:
		return 1.5
	if itemString.find("crysknife") != -1 or itemString.find("crysknives") != -1:
		return 5.5
	if itemString.find("knife") != -1 or itemString.find("knives") != -1 or itemString.find("shito") != -1:
		return 1.5
	if itemString.find("stiletto") != -1:
		return 1.5
	if itemString.find("scalpel") != -1:
		return 2
	# Pick-axes
	if itemString.find("pick-axe") != -1:
		return 2
	if itemString.find("dwarvish mattock") != -1 or itemString.find("broad pick"):
		return 11.5
	# Short swords
	if itemString.find("orcish short sword") != -1 or itemString.find("crude short sword") != -1:
		return 4.5
	if itemString.find("dwarvish short sword") != -1 or itemString.find("broad short sword") != -1:
		return 4.5
	if itemString.find("elven short sword") != -1 or itemString.find("runed short sword") != -1:
		return 4.5
	if itemString.find("short sword") != -1 or itemString.find("wakizashi") != -1:
		return 4.5
	# Broadswords
	# NOTE: "runed broadswords" can refer to either runeswords or elven broadswords,
	# but since runeswords other than Stormbringer can only be found by wishing,
	# we'll just assume arbitrary runed broadswords are elven broadswords.
	if itemString.find("runed broadsword") != -1 or itemString.find("elven broadsword") != -1:
		return 4.5
	if itemString.find("runesword") != -1:
		return 4.5
	if itemString.find("broadsword") != -1 or itemString.find("ninja-to") != -1:
		return 4.5
	# Long swords
	if itemString.find("long sword") != -1:
		return 6.5
	if itemString.find("katana") != -1 or itemString.find("samurai sword") != -1:
		return 6.5
	# Two-handed swords
	if itemString.find("two-handed sword") != -1:
		return 10.5
	if itemString.find("tsurugi") != -1 or itemString.find("long samurai sword") != -1:
		return 11.5
	# Scimitars
	if itemString.find("scimitar") != -1 or itemString.find("curved sword") != -1:
		return 4.5
	# Sabers
	if itemString.find("silver saber") != -1:
		return 4.5
	# Clubs
	if itemString.find("aklys") != -1 or itemString.find("thonged club") != -1:
		return 2
	if itemString.find("club") != -1:
		return 2
	# Maces
	if itemString.find("mace") != -1:
		return 3.5
	# Morning stars
	if itemString.find("morning star") != -1:
		return 4.5
	# Flails
	if itemString.find("flail") != -1 or itemString.find("nunchaku") != -1:
		return 5
	if itemString.find("grappling hook") != -1 or itemString.find("iron hook") != -1:
		return 3.5
	# Hammers
	if itemString.find("war hammer") != -1:
		return 2.5
	# Staves
	if itemString.find("staff") != -1 or itemString.find("staves") != -1:
		return 3.5
	# Polearms
	if itemString.find("partisan") != -1 or itemString.find("vulgar polearm") != -1:
		return 4.5
	if itemString.find("fauchard") != -1 or itemString.find("pole sickle") != -1:
		return 4.5
	if itemString.find("glaive") != -1 or itemString.find("naginata") != -1 or itemString.find("single-edged polearm") != -1:
		return 5.5
	if itemString.find("bec-de-corbin") != -1 or itemString.find("beaked polearm") != -1:
		return 3.5
	if itemString.find("spetum") != -1 or itemString.find("forked polearm") != -1:
		return 7
	if itemString.find("lucern hammer") != -1 or itemString.find("pronged polearm") != -1:
		return 3.5
	if itemString.find("bill-guisarme") != -1 or itemString.find("hooked polearm") != -1:
		return 5.5
	if itemString.find("guisarme") != -1 or itemString.find("pruning hook") != -1:
		return 4.5
	if itemString.find("ranseur") != -1 or itemString.find("hilted polearm") != -1:
		return 5
	if itemString.find("voulge") != -1 or itemString.find("pole cleaver") != -1:
		return 5
	if itemString.find("bardiche") != -1 or itemString.find("long poleaxe") != -1:
		return 7.5
	if itemString.find("halberd") != -1 or itemString.find("angled poleaxe") != -1:
		return 7
	# Axes
	if itemString.find("battle-axe") != -1:
		return 8.5
	if itemString.find("axe") != -1:
		return 2.5
	# Spears
	if itemString.find("orcish spear") != -1 or itemString.find("crude spear") != -1:
		return 4.5
	if itemString.find("elven spear") != -1 or itemString.find("runed spear") != -1:
		return 4.5
	if itemString.find("dwarven spear") != -1 or itemString.find("stout spear") != -1:
		return 4.5
	if itemString.find("javelin") != -1 or itemString.find("throwing spear") != -1:
		return 3.5
	if itemString.find("silver spear") != -1:
		return 4.5
	if itemString.find("spear") != -1:
		return 4.5
	# Tridents
	if itemString.find("trident") != -1:
		return 7.5
	# Lances
	if itemString.find("lance") != -1:
		return 4.5
	# Crossbow
	if itemString.find("crossbow bolt") != -1:
		return 4.5
	if itemString.find("crossbow") != -1:
		return 1.5
	# Archery
	if itemString.find("orcish bow") != -1 or itemString.find("crude bow") != -1:
		return 1.5
	if itemString.find("orcish arrow") != -1 or itemString.find("crude arrow") != -1:
		return 3.5
	if itemString.find("elven bow") != -1 or itemString.find("runed bow") != -1:
		return 1.5
	if itemString.find("elven arrow") != -1 or itemString.find("runed arrow") != -1:
		return 3.5
	if itemString.find("yumi") != -1 or itemString.find("long bow") != -1:
		return 1.5
	if itemString.find("ya") != -1 or itemString.find("bamboo arrow") != -1:
		return 4
	if itemString.find("silver arrow") != -1:
		return 3.5
	if itemString.find("bow") != -1:
		return 1.5
	if itemString.find("arrow") != -1:
		return 3.5
	# Sling
	if itemString.find("sling") != -1:
		return 1.5
	if itemString.find("flint stone") != -1:
		return 3.5
	# Dart
	if itemString.find("dart") != -1:
		return 1.5
	# Shuriken
	if itemString.find("shuriken") != -1 or itemString.find("throwing star"):
		return 3.5
	# Boomerang
	if itemString.find("boomerang") != -1:
		return 5
	# Whip
	if itemString.find("whip") != -1:
		return 1
	if itemString.find("rubber hose") != -1:
		return 2
	# Unicorn Horn
	if itemString.find("unicorn horn") != -1:
		return 6.5
	# TODO: Recognize artifacts
	return -999 # not a weapon

def baseWeaponToHit(itemString):
	# Daggers
	if itemString.find("orcish dagger") != -1 or itemString.find("crude dagger") != -1:
		return 2
	if itemString.find("silver dagger") != -1:
		return 2
	if itemString.find("elven dagger") != -1 or itemString.find("runed dagger") != -1:
		return 2
	if itemString.find("dagger") != -1:
		return 2
	if itemString.find("athame") != -1:
		return 2
	# Knives
	if itemString.find("crysknife") != -1 or itemString.find("crysknives") != -1:
		return 3
	if itemString.find("scalpel") != -1:
		return 2
	# Pick-axes
	if itemString.find("dwarvish mattock") != -1 or itemString.find("broad pick"):
		return -1
	# Long swords
	if itemString.find("katana") != -1 or itemString.find("samurai sword") != -1:
		return 1
	# Two-handed swords
	if itemString.find("tsurugi") != -1 or itemString.find("long samurai sword") != -1:
		return 2
	# Archery
	if itemString.find("ya") != -1 or itemString.find("bamboo arrow") != -1:
		return 1
	# Shuriken
	if itemString.find("shuriken") != -1 or itemString.find("throwing star"):
		return 2
	# Unicorn Horn
	if itemString.find("unicorn horn") != -1:
		return 1
	# TODO: Recognize artifacts
	return 0 # All non-artifact weapons not listed above have +0 to hit