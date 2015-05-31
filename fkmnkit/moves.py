from enum import Enum

class MoveCategory(Enum):
	PHYSICAL = 0
	SPECIAL = 1
	STATUS = 2

class PokeMove:
	def __init__(self, label='', move_cat=MoveCategory.PHYSICAL, bp=0, accuracy=100, efftype=None, stabtype=None):
		pass

	def applicable_stab(self, pkmn):
		#need stabtype because pokes like Hawlucha don't get double STAB from dual type
		if self.stabtype in pkmn.types:
			if len(pkmn.types) > 1:
				return 1.25
			else:
				return 1.5
		else:
			return 1
