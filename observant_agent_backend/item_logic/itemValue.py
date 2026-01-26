#!/usr/bin/env python3

# TODO

# Calls functions in the other files in this folder.
# Ideally, the main agent logic should only have to import this file, not any of the others.

# As a general rule, when the agent is carrying too much stuff, items with the lowest value are the first to go.

# The value of an item tends to depend on what else is in the inventory.
# For example, once the agent has lots of food, further food should be assigned lower value.
# For this purpose, an item should not treat itself as part of the inventory.
# If the agent has 2 food rations, each food ration should be valued as if 1 food ration is in the inventory.
# This way, the value of an item doesn't change when it moves between floor and inventory.

# It would be cool if we could use "value" to indicate the maximum price the agent is willing to pay for something,
# but I highly doubt I can do a remotely good job estimating that...