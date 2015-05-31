from enum import Enum
from fkmnkit.moves import MoveCategory
from fkmnkit.poketypes import PokeTypeSet

class StatID(Enum):
	HP = 0
	ATK = 1
	DFN = 2
	SATK = 3
	SDFN = 4
	SPD = 5
	ACC = 6
	EVA = 7

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
	MAX_STAT_STAGE = 6
	MIN_STAT_STAGE = -6

	def _get_stage_mult(self, d, sid):
		if sid == StatID.EVA:
			if d < 0:
				return (3 - d) / 3
			elif d == 0:
				return 1
			else:
				return 3 / (3 + d)
		elif sid == StatID.ACC:
			if d < 0:
				return 3 / (3 + d)
			elif d == 0:
				return 1
			else:
				return (3 - d) / 3
		else:
			if d < 0:
				return 2 / (2 - d)
			elif d == 0:
				return 1
			else:
				return (2 + d) / 2

	def _validate_stat_lvl(self, d):
		return not (d < PokemonInstance.MIN_STAT_STAGE or d > PokemonInstance.MAX_STAT_STAGE)

	def _validate_lvl(self, d):
		return not (d < PokemonInstance.MIN_LVL or d > PokemonInstance.MAX_LVL)

	def _validate_ev_ttl(self, d):
		return (self.hpev + self.atkev + self.dfnev + self.satkev + self.sdfnev + self.spdev) <= PokemonInstance.MAX_EVS_TOTAL

	def _validate_ev_val(self, d):
		return d <= PokemonInstance.MAX_EVS_PER_STAT

	def _validate_iv_val(self, d):
		return not (d < PokemonInstance.MIN_BST_VAL or d > PokemonInstance.MAX_BST_VAL)

	def _calculate_stat(self, iv, bsv, evs, lvloffset=0, foffset=5, nature=0):
		return ((iv + 2* bsv + evs/4 + lvloffset) * self.level / 100 + foffset) * (1.0 + nature * 0.1)

	def attacks_with(self, technique, *targets):
		damages = []

		for target in targets:
			if technique.move_kind == MoveCategory.PHYSICAL and bp > 0:
				a_d_ratio = self.attack / target.defense
			elif technique.move_kind == MoveCategory.SPECIAL and bp > 0:
				a_d_ratio = self.sattack / target.sdefense
			else:
				damages.append(technique.custom_damage(*targets))
				continue

			#critical hits are not applied in here, they're to be calculated outside
			#in an actual battle simulator

			stab = 1.5 if technique.stabtype in self.types else 1
			dmg_modifier = technique.efftypes.effective_against(target.types)
			dmg = ((2*self.level+10) * a_d_ratio * technique.bp + 2) * dmg_modifier * stab
			damages.append((0.85*dmg, dmg))

		return damages
