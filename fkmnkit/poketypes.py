import gettext
import csv
import os
from collections import Counter

gettext.install('fakemon_kit')

class PokeMove:
	PHYSICAL = 0
	SPECIAL = 1
	STATUS = 2
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
	MIN_BST_VAL=1
	MAX_BST_VAL=256
	def __init__(self, label='', dexno=0, regionno=0, genno=0, egggrps=None, 
	             abilities=None, types=None, bhp=MIN_BST_VAL, batk=MIN_BST_VAL, 
	             bdfn=MIN_BST_VAL, bsatk=MIN_BST_VAL, bsdfn=MIN_BST_VAL, bspd=MIN_BST_VAL):
		#hash should be calculated by dexno and genno due to intro of mega-evos

		self.label = label
		self.dexno = dexno
		self.regionno = regionno
		self.genno = genno

		self.bhp = bhp
		self.batk = batk
		self.bdfn = bdfn
		self.bsatk = bsatk
		self.bsdfn = bsdfn
		self.bspd = bspd

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

	def _validate_bst_val(self, d):
		return not (d < Pokemon.MIN_BST_VAL or d > Pokemon.MAX_BST_VAL)

	@property
	def bhp(self):
		return self._bhp

	@bhp.setter
	def bhp(self, d):
		if not self._validate_bst_val(d):
			raise ValueError("Base stats cannot go below 1 or above 256!")
		self._bhp = d

	@property
	def batk(self):
		return self._batk

	@batk.setter
	def batk(self, d):
		if not self._validate_bst_val(d):
			raise ValueError("Base stats cannot go below 1 or above 256!")
		self._batk = d

	@property
	def bdfn(self):
		return self._bdfn

	@bdfn.setter
	def bdfn(self, d):
		if not self._validate_bst_val(d):
			raise ValueError("Base stats cannot go below 1 or above 256!")
		self._bdfn = d

	@property
	def bsatk(self):
		return self._bsatk

	@bsatk.setter
	def bsatk(self, d):
		if not self._validate_bst_val(d):
			raise ValueError("Base stats cannot go below 1 or above 256!")
		self._bsatk = d

	@property
	def bsdfn(self):
		return self._bsdfn

	@bsdfn.setter
	def bsdfn(self, d):
		if not self._validate_bst_val(d):
			raise ValueError("Base stats cannot go below 1 or above 256!")
		self._bsdfn = d

	@property
	def bspd(self):
		return self._bspd

	@bspd.setter
	def bspd(self, d):
		if not self._validate_bst_val(d):
			raise ValueError("Base stats cannot go below 1 or above 256!")
		self._bspd = d

class PokemonInstance:
	MIN_LVL = 1
	MAX_LVL = 100
	MAX_IVS = 31
	MAX_EVS_PER_STAT = 252
	MAX_EVS_TOTAL = 510

	def _validate_lvl(self, d):
		return not (d < PokemonInstance.MIN_LVL or d > PokemonInstance.MAX_LVL)

	def _validate_ev_ttl(self, d):
		return (self.hpev + self.atkev + self.dfnev + self.satkev + self.sdfnev + self.spdev) <= PokemonInstance.MAX_EVS_TOTAL

	def _validate_ev_val(self, d):
		return d <= PokemonInstance.MAX_EVS_PER_STAT

	def _validate_iv_val(self, d):
		return not (d < PokemonInstance.MIN_BST_VAL or d > PokemonInstance.MAX_BST_VAL)

	def _calculate_stat(self, iv, bsv, evs, offset=5, nature=0):
		return ((iv + 2* bsv + evs/4) * self.level / 100 + offset) * (1.0 + nature * 0.1)

	def attacks_with(self, technique, *targets):
		damages = []

		for target in targets:
			if technique.move_kind == PokeMove.PHYSICAL and bp > 0:
				a_d_ratio = self.attack / target.defense
			elif technique.move_kind == PokeMove.SPECIAL and bp > 0:
				a_d_ratio = self.sattack / target.sdefense
			else:
				damages.append(technique.custom_damage(*targets))
				continue

			#critical hits are not applied in here, they're to be calculated outside
			#in an actual battle simulator

			stab = 1.5 if technique.stabtype in self.types else 1
			dmg_modifier = technique.efftype.effective_against(target.types)
			dmg = ((2*self.level+10) * a_d_ratio * technique.bp + 2) * dmg_modifier * stab
			damages.append((0.85*dmg, dmg))

		return damages

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
