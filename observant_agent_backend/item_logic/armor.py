#!/usr/bin/env python3

# TODO

# The value of an armor is determined by the following:
	# its AC contribution (bigger AC decrease = more value)
	# whether it's physically possible to wear it at the moment (no = less value)
	# its weight (more weight = less value)
	# if it has beneficial properties like speed or jumping (yes = more value)
	# if it's cursed (yes = less value)
		# (an armor being cursed should apply a flat penalty to total value.)
		# (if an armor is super strong on its own merit, we might wear it despite the curse.)
	# if we have a better armor for that slot already (yes = less value)
		# an armor having beneficial properties mitigates this somewhat
	# if it's metallic (yes = less value, because it interferes with spellcasting)
		# if we're a spellcaster class or it's later in the game, we care about this more
	# if it's a T-shirt (yes = more value)
		# T-shirts do nothing early, but are invaluable once you can enchant things easily
	# whether the agent is a monk and the armor would interfere with doing monk things (yes = MUCH less value)