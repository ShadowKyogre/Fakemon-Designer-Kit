import gettext
import csv
import os
from collections import Counter
from itertools import product

gettext.install('fakemon_kit')

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

	def effectiveness_against(self, other):
		#implement corrections through multiplier overriding?
		#print('PokeType.effectiveness_against', other)
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
				running_product *= self.effectiveness_against(t)
			return running_product
		else:
			raise ValueError("Cannot calculate type effectiveness")

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

	def effectiveness_against(self, other):
		#print('effectiveness_against', other)
		if isinstance(other, PokeTypeSet):
			running_product = 1
			for t in self.types: #attack types
				for t2 in other.types: #defend types
					running_product *= t.effectiveness_against(t2)
			return running_product
		elif isinstance(other, PokeType):
			running_product = 1
			for t in self.types: #attack types
				running_product *= t.effectiveness_against(other)
			return running_product
		else:
			raise ValueError("Cannot calculate type effectiveness")

def check_coverage(types_or_type_sets, pokemon, consider_abilities=False):
	no_effect = []
	not_very_effective = []
	normal_effective = []
	super_effective = []

	for pkmn in pokemon:
		greatest_effectiveness = 0
		for titem in types_or_type_sets:
			if titem.effectiveness_against(pkmn.types) > greatest_effectiveness:
				greatest_effectiveness = titem.effectiveness_against(pkmn.types)

		if greatest_effectiveness == 0:
			no_effect.append(pkmn)
		elif greatest_effectiveness < 1:
			not_very_effective.append(pkmn)
		elif greatest_effectiveness >= 2:
			super_effective.append(pkmn)
		else:
			normal_effective.append(pkmn)

	return [no_effect, not_very_effective, normal_effective, super_effective]

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
