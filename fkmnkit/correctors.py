from fkmnkit.poketypes import PokeType, PokeTypeSet
from copy import deepcopy

def toInverseType(poketype):
	new_weaknesses = poketype.resistances|poketype.immunities
	new_resistances = poketype.weaknesses

	new_type = PokeType(tid=poketype.tid, weaknesses=new_weaknesses, resistances=new_resistances, label=poketype.label)
	return new_type

def toInverseTypeSet(poketypeset):
	itypes = []
	for i in poketypeset.types:
		itypes.append(toInverseType(poketype))
	return PokeTypeSet(itypes)

def toWonderSet(poketypesset):
	wtypes = []
	for t in poketypeset.types:
		wtypes.append(WonderType(t))
	return PokeTypeSet(wtypes)

class WonderType(PokeType):
	"""Correctors are applied to attacking type!"""
	def __init__(self, orig_type):
		super().__init__(tid=orig_type.tid, weaknesses=orig_type.weaknesses, 
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
				print(running_product, self, t)
				running_product *= super().__mul__(t)
			if running_product >= 2:
				return running_product
			else:
				return 0
		else:
			return other

class OverwriteType(PokeType):
	"""Correctors are applied to attacking type!
	This is useful for things like freeze-dry, synchronoise, dry-skin, etc. However,
	synchronoise might be more efficient as its own corrector. Should it be?
	"""
	def __init__(self, orig_type, orw=None, orr=None, ori=None):
		super().__init__(orig_type.tid, weaknesses=orig_type.weaknesses, 
		                 resistances=orig_type.resistances, immunities=orig_type.immunities,
		                 label=orig_type.label)
		if orw is None:
			self.orw = set()
		else:
			self.orw = orw

		if orr is None:
			self.orr = set()
		else:
			self.orr = orr

		if ori is None:
			self.ori = set()
		else:
			self.ori = ori

	def __mul__(self, other):
		#implement corrections through multiplier overriding?
		#print('OverwriteType.__mul__', other)
		if isinstance(other, PokeType): #defending type
			if other in self.orw: #force the defending type to be weak to this
				return 2
			elif other in self.orr: #force the defending type to be resistant to this
				return 0.5
			elif other in self.ori: #force the defending type to be immune to this
				return 0
			else:
				return super().__mul__(other)
		elif isinstance(other, PokeTypeSet):
			running_product = 1
			for t in other.types: #defending types
				running_product *= (self * t)
			return running_product
		else:
			return other
