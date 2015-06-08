from enum import Enum
from math import floor

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
			raise ValueError("Base stats cannot go below {} or above {}!".format(Pokemon.MIN_BST_VAL, Pokemon.MAX_BST_VAL))
		self._bhp = d

	@property
	def batk(self):
		return self._batk

	@batk.setter
	def batk(self, d):
		if not self._validate_bst_val(d):
			raise ValueError("Base stats cannot go below {} or above {}!".format(Pokemon.MIN_BST_VAL, Pokemon.MAX_BST_VAL))
		self._batk = d

	@property
	def bdfn(self):
		return self._bdfn

	@bdfn.setter
	def bdfn(self, d):
		if not self._validate_bst_val(d):
			raise ValueError("Base stats cannot go below {} or above {}!".format(Pokemon.MIN_BST_VAL, Pokemon.MAX_BST_VAL))
		self._bdfn = d

	@property
	def bsatk(self):
		return self._bsatk

	@bsatk.setter
	def bsatk(self, d):
		if not self._validate_bst_val(d):
			raise ValueError("Base stats cannot go below {} or above {}!".format(Pokemon.MIN_BST_VAL, Pokemon.MAX_BST_VAL))
		self._bsatk = d

	@property
	def bsdfn(self):
		return self._bsdfn

	@bsdfn.setter
	def bsdfn(self, d):
		if not self._validate_bst_val(d):
			raise ValueError("Base stats cannot go below {} or above {}!".format(Pokemon.MIN_BST_VAL, Pokemon.MAX_BST_VAL))
		self._bsdfn = d

	@property
	def bspd(self):
		return self._bspd

	@bspd.setter
	def bspd(self, d):
		if not self._validate_bst_val(d):
			raise ValueError("Base stats cannot go below {} or above {}!".format(Pokemon.MIN_BST_VAL, Pokemon.MAX_BST_VAL))
		self._bspd = d

class Nature:
	def __init__(self, boost, detriment, boost_val=1, detriment_val=1):
		self.boost = boost
		self.boost_val = boost_val

		self.detriment = detriment
		self.detriment_val = detriment_val

	def get_bonus(self, stat_id):
		multi = 0
		if stat_id == self.boost:
			multi += self.boost_val
		if stat_id == self.detriment:
			multi -= self.detriment_val
		return multi

class PokemonInstance:
	MIN_LVL = 1
	MAX_LVL = 100
	MAX_IVS = 31
	MAX_EVS_PER_STAT = 252
	MAX_EVS_TOTAL = 510
	MAX_STAT_STAGE = 6
	MIN_STAT_STAGE = -6

	def __init__(self, pokedex_data, hp_iv=0, atk_iv=0, dfn_iv=0, satk_iv=0, sdfn_iv=0, spd_iv=0, 
	              hp_ev=0, atk_ev=0, dfn_ev=0, satk_ev=0, sdfn_ev=0, spd_ev=0,   
	             current_hp=-1, nature=None):
		self.pokedex_data = pokedex_data
		self.nature = nature

		self.hp_iv = hp_iv
		self.atk_iv = atk_iv
		self.dfn_iv = dfn_iv
		self.satk_iv = satk_iv
		self.sdfn_iv = sdfn_iv
		self.spd_iv = spd_iv

		self.hp_ev = hp_ev
		self.atk_ev = atk_ev
		self.dfn_ev = dfn_ev
		self.satk_ev = satk_ev
		self.sdfn_ev = sdfn_ev
		self.spd_ev = spd_ev

	@property
	def hp(self):
		return self._calculate_stat(self.hp_iv, self.pokedex_data.bhp, self.hp_ev, lvloffset=100, foffset=10)

	@property
	def atk(self):
		return self._calculate_stat(self.atk_iv, self.pokedex_data.batk, self.atk_ev, nature=self.nature.get_bonus(StatID.ATK))

	@property
	def dfn(self):
		return self._calculate_stat(self.dfn_iv, self.pokedex_data.bdfn, self.dfn_ev, nature=self.nature.get_bonus(StatID.DFN))

	@property
	def satk(self):
		return self._calculate_stat(self.satk_iv, self.pokedex_data.bsatk, self.satk_ev, nature=self.nature.get_bonus(StatID.SATK))

	@property
	def sdfn(self):
		return self._calculate_stat(self.sdfn_iv, self.pokedex_data.bsdfn, self.sdfn_ev, nature=self.nature.get_bonus(StatID.SDFN))

	@property
	def spd(self):
		return self._calculate_stat(self.spd_iv, self.pokedex_data.bspd, self.spd_ev, nature=self.nature.get_bonus(StatID.SPD))

	@property
	def hp_iv(self):
		return self._hp_iv

	@hp_iv.setter
	def hp_iv(self, d):
		if not self._validate_iv_val(d):
			raise ValueError("IVs cannot go below 0 or above {}!".format(PokemonInstance.MAX_IVS))
		self._hp_iv = d

	@property
	def atk_iv(self):
		return self._atk_iv

	@atk_iv.setter
	def atk_iv(self, d):
		if not self._validate_iv_val(d):
			raise ValueError("IVs cannot go below 0 or above {}!".format(PokemonInstance.MAX_IVS))
		self._atk_iv = d

	@property
	def dfn_iv(self):
		return self._dfn_iv

	@dfn_iv.setter
	def dfn_iv(self, d):
		if not self._validate_iv_val(d):
			raise ValueError("IVs cannot go below 0 or above {}!".format(PokemonInstance.MAX_IVS))
		self._dfn_iv = d

	@property
	def satk_iv(self):
		return self._satk_iv

	@satk_iv.setter
	def satk_iv(self, d):
		if not self._validate_iv_val(d):
			raise ValueError("IVs cannot go below 0 or above {}!".format(PokemonInstance.MAX_IVS))
		self._satk_iv = d

	@property
	def sdfn_iv(self):
		return self._sdfn_iv

	@sdfn_iv.setter
	def sdfn_iv(self, d):
		if not self._validate_iv_val(d):
			raise ValueError("IVs cannot go below 0 or above {}!".format(PokemonInstance.MAX_IVS))
		self._sdfn_iv = d

	@property
	def spd_iv(self):
		return self._spd_iv

	@spd_iv.setter
	def spd_iv(self, d):
		if not self._validate_iv_val(d):
			raise ValueError("IVs cannot go below 0 or above {}!".format(PokemonInstance.MAX_IVS))
		self._spd_iv = d

	@property
	def hp_ev(self):
		return self._hp_ev

	@hp_ev.setter
	def hp_ev(self, d):
		if not self._validate_ev_val(d):
			raise ValueError("EVs cannot go below 0 or above {}!".format(PokemonInstance.MAX_EVS_PER_STAT))
		if not self._validate_ev_ttl(hp_ev=d):
			raise ValueError("EV Values exceed maximum total!")
		self._hp_ev = d

	@property
	def atk_ev(self):
		return self._atk_ev

	@atk_ev.setter
	def atk_ev(self, d):
		if not self._validate_ev_val(d):
			raise ValueError("EVs cannot go below 0 or above {}!".format(PokemonInstance.MAX_EVS_PER_STAT))
		if not self._validate_ev_ttl(atk_ev=d):
			raise ValueError("EV Values exceed maximum total!")
		self._atk_ev = d

	@property
	def dfn_ev(self):
		return self._dfn_ev

	@dfn_ev.setter
	def dfn_ev(self, d):
		if not self._validate_ev_val(d):
			raise ValueError("EVs cannot go below 0 or above {}!".format(PokemonInstance.MAX_EVS_PER_STAT))
		if not self._validate_ev_ttl(dfn_ev=d):
			raise ValueError("EV Values exceed maximum total!")
		self._dfn_ev = d

	@property
	def satk_ev(self):
		return self._satk_ev

	@satk_ev.setter
	def satk_ev(self, d):
		if not self._validate_ev_val(d):
			raise ValueError("EVs cannot go below 0 or above {}!".format(PokemonInstance.MAX_EVS_PER_STAT))
		if not self._validate_ev_ttl(satk_ev=d):
			raise ValueError("EV Values exceed maximum total!")
		self._satk_ev = d

	@property
	def sdfn_ev(self):
		return self._sdfn_ev

	@sdfn_ev.setter
	def sdfn_ev(self, d):
		if not self._validate_ev_val(d):
			raise ValueError("EVs cannot go below 0 or above {}!".format(PokemonInstance.MAX_EVS_PER_STAT))
		if not self._validate_ev_ttl(sdfn_ev=d):
			raise ValueError("EV Values exceed maximum total!")
		self._sdfn_ev = d

	@property
	def spd_ev(self):
		return self._spd_ev

	@spd_ev.setter
	def spd_ev(self, d):
		if not self._validate_ev_val(d):
			raise ValueError("EVs cannot go below 0 or above {}!".format(PokemonInstance.MAX_EVS_PER_STAT))
		if not self._validate_ev_ttl(spd_ev=d):
			raise ValueError("EV Values exceed maximum total!")
		self._spd_ev = d

	@property
	def level(self):
		return self._level

	@level.setter
	def level(self, d):
		if not self._validate_lvl(d):
			raise ValueError("Level must be between {} and {}".format(PokemonInstance.MIN_LVL, PokemonInstance.MAX_LVL))
		else:
			self._level = d

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

	def _validate_ev_ttl(self, hp_ev=None, atk_ev=None, dfn_ev=None, satk_ev=None, sdfn_ev=None, spd_ev=None):
		if hp_ev is None:
			hp_ev = self.hp_ev if hasattr(self, 'hp_ev') else 0
		if atk_ev is None:
			atk_ev = self.atk_ev if hasattr(self, 'atk_ev') else 0
		if dfn_ev is None:
			dfn_ev = self.dfn_ev if hasattr(self, 'dfn_ev') else 0
		if satk_ev is None:
			satk_ev = self.satk_ev if hasattr(self, 'satk_ev') else 0
		if sdfn_ev is None:
			sdfn_ev = self.sdfn_ev if hasattr(self, 'sdfn_ev') else 0
		if spd_ev is None:
			spd_ev = self.spd_ev if hasattr(self, 'spd_ev') else 0
		return (hp_ev + atk_ev + dfn_ev + satk_ev + sdfn_ev + spd_ev) <= PokemonInstance.MAX_EVS_TOTAL

	def _validate_ev_val(self, d):
		return 0 <= d <= PokemonInstance.MAX_EVS_PER_STAT

	def _validate_iv_val(self, d):
		return not (d < 0 or d > PokemonInstance.MAX_IVS)

	def _calculate_stat(self, iv, bsv, evs, lvloffset=0, foffset=5, nature=0):
		return floor( floor((iv + 2* bsv + evs/4 + lvloffset) * self.level / 100 + foffset) * (1.0 + nature * 0.1) )

	def attacks_with(self, technique, *targets):
		damages = []

		for target in targets:
			if technique.move_kind == MoveCategory.PHYSICAL and dbp > 0:
				a_d_ratio = self.attack / target.defense
			elif technique.move_kind == MoveCategory.SPECIAL and dbp > 0:
				a_d_ratio = self.sattack / target.sdefense
			else:
				damages.append(technique.custom_damage(self, target))
				continue

			#critical hits are not applied in here, they're to be calculated outside
			#in an actual battle simulator

			stab = 1.5 if technique.stabtype in self.types else 1
			dmg_modifier = technique.efftypes.effective_against(target.types)
			dmg = ((2*self.level+10) * a_d_ratio * technique.bp(self, target) + 2) * dmg_modifier * stab
			damages.append((0.85*dmg, dmg))

		return damages
