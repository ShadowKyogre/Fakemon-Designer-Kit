import gettext
import csv
import os
from collections import Counter

gettext.install('fakemon_kit')

class PokeMove:
	PHYSICAL = 0
	SPECIAL = 0
	STATUS = 0
	def __init__(self, label='', move_kind=0, bp=0, accuracy=100, efftype=None, stabtype=None):
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

class Pokemon:
	def __init__(self, label='', dexno=0, regionno=0, genno=0, egggrps=None, 
	             abilities=None, types=None, hp=1, atk=1, dfn=1, satk=1, sdfn=1, spd=1):
		#hash should be calculated by dexno and genno due to intro of mega-evos

		self.label = label
		self.dexno = dexno
		self.regionno = regionno
		self.genno = genno

		self.hp = hp
		self.atk = atk
		self.dfn = dfn
		self.satk = satk
		self.sdfn = sdfn
		self.spd = spd

		if types is None:
			self.types = PokeTypeSet([])
		else:
			self.types = types

		if egggrps is None:
			self.egggrps = set()
		else:
			self.egggrps = egggrps

		if abilities is None:
			self.abilities = []
		else:
			self.abilities = abilities

class PokeType:
	def __init__(self, tid=0, weaknesses=None, resistances=None, immunities=None, label=''):
		self.tid = tid
		self.label = label

		if weaknesses is None:
			self.weaknesses = set()
		else:
			self.weaknesses = weaknesses

		if resistances is None:
			self.resistances = set()
		else:
			self.resistances = resistances

		if immunities is None:
			self.immunities = set()
		else:
			self.immunities = immunities

	def __hash__(self):
		return self.tid

	def __str__(self):
		return "Pokemon Type {}: {} weaknesses, {} immunities, {} resistances".format(self.label, len(self.weaknesses), len(self.immunities), len(self.resistances))

	def __repr__(self):
		return "PokeType(tid={}, label={})".format(self.tid, self.label)

	def __mul__(self, other):
		#implement corrections through multiplier overriding?
		#print('PokeType.__mul__', other)
		if isinstance(other, PokeType): #defending type
			if self in other.weaknesses:
				return 2
			elif self in other.resistances:
				return 0.5
			elif self in other.immunities:
				return 0
			else:
				return 1
		elif isinstance(other, PokeTypeSet):
			running_product = 1
			for t in other.types: #defending types
				running_product *= (self * t)
			return running_product
		else:
			return other

	def __eq__(self, other):
		if isinstance(other, PokeType):
			return self.tid == other.tid
		else:
			return False

class PokeTypeSet:
	def __init__(self, types):
		self.types = set()
		for t in types:
			self.types.add(t)

	def __str__(self):
		return "Pokemon Type Combo: {}".format('/'.join(t.label for t in self.types))

	def __repr__(self):
		return "PokeTypeSet({})".format(repr(self.types))

	def __mul__(self, other):
		#print('__mul__', other)
		if isinstance(other, PokeTypeSet):
			running_product = 1
			for t in self.types: #attack types
				for t2 in other.types: #defend types
					running_product *= (t * t2)
			return running_product
		elif isinstance(other, PokeType):
			running_product = 1
			for t in self.types: #attack types
				running_product *= (t * other)
			return running_product
		else:
			return other

STANDARD_TYPES = {}
with open(os.path.join(os.path.dirname(__file__), 'standard_types.tsv'), 'r', encoding='utf-8') as f:
	csvr = csv.reader(f, delimiter='\t')
	come_back_here=[]
	tid=0
	for row in csvr:
		come_back_here.append([ float(i) for i in row[1:] ])
		durpy = PokeType(tid=tid, label=row[0])
		STANDARD_TYPES[tid] = durpy
		STANDARD_TYPES[row[0]] = durpy
		tid += 1
	else:
		for heretype, cbh in enumerate(come_back_here):
			for puttype, efx in enumerate(cbh):
				if efx == 0.5:
					STANDARD_TYPES[puttype].resistances.add(STANDARD_TYPES[heretype])
				elif efx == 0:
					STANDARD_TYPES[puttype].immunities.add(STANDARD_TYPES[heretype])
				elif efx == 2:
					STANDARD_TYPES[puttype].weaknesses.add(STANDARD_TYPES[heretype])
