from poketypes import PokeType, PokeTypeSet

def toWonderSet(poketypesset):
	wtypes = []
	for t in poketypeset.types:
		wtypes.append(WonderType(t))
	return PokeTypeSet(wtypes)

class WonderType(PokeType):
	"""Correctors are applied to attacking type!"""
	def __init__(self, orig_type):
		super().__init__(orig_type.tid, weaknesses=orig_type.weaknesses, 
		                 resistances=orig_type.resistances, immunities=orig_type.immunities,
		                 label=orig_type.label)

	def __mul__(self, other):
		#implement corrections through multiplier overriding?
		#print('WonderType.__mul__', other)
		if isinstance(other, PokeType): #defending type
			if self in other.weaknesses:
				return 2
			else:
				return 0
		elif isinstance(other, PokeTypeSet):
			running_product = 1
			for t in other.types: #defending types
				#res = (self * t)
				#print("HURP", super().__mul__(t))
				running_product *= super().__mul__(t)
			if running_product >= 2:
				return running_product
			else:
				return 0
		else:
			return other


