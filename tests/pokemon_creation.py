import unittest

import fkmnkit
from fkmnkit.creatures import Pokemon, PokemonInstance, Nature, StatID

class TestPokemonCreation(unittest.TestCase):
	def test_bst_validation(self):
		with self.assertRaises(ValueError):
			Pokemon(bhp=300)

		actual_pokemon = Pokemon(bhp=200)
		self.assertEquals(actual_pokemon.bhp, 200)

	def test_iv_validation(self):
		actual_pokemon = Pokemon(bhp=200)

		with self.assertRaises(ValueError):
			PokemonInstance(actual_pokemon, hp_iv=32)

		with self.assertRaises(ValueError):
			PokemonInstance(actual_pokemon, hp_iv=-1)

		actual_pokemoni = PokemonInstance(actual_pokemon, hp_iv=16)
		self.assertEquals(actual_pokemoni.hp_iv, 16)

	def test_ev_validation(self):
		actual_pokemon = Pokemon(bhp=200)

		with self.assertRaises(ValueError):
			PokemonInstance(actual_pokemon, hp_ev=253)

		with self.assertRaises(ValueError):
			PokemonInstance(actual_pokemon, hp_ev=168, atk_ev=168, dfn_ev=168, spd_ev=168)

		with self.assertRaises(ValueError):
			PokemonInstance(actual_pokemon, hp_ev=-1)

		actual_pokemoni = PokemonInstance(actual_pokemon, hp_ev=168)
		self.assertEquals(actual_pokemoni.hp_ev, 168)

		actual_pokemoni = PokemonInstance(actual_pokemon, hp_ev=168, atk_ev=168, dfn_ev=168, spd_ev=6)
		self.assertEquals(actual_pokemoni.hp_ev, 168)
		self.assertEquals(actual_pokemoni.atk_ev, 168)
		self.assertEquals(actual_pokemoni.dfn_ev, 168)
		self.assertEquals(actual_pokemoni.spd_ev, 6)

	def test_hp_stat_calculation(self):
		wigglytuff = Pokemon(bhp=140, batk=70, bdfn=45, bsatk=85, bsdfn=50, bspd=45)
		wigglytuff_instance = PokemonInstance(wigglytuff)

		wigglytuff_instance.level = 50
		self.assertEquals(wigglytuff_instance.hp, 200)

		wigglytuff_instance.level = 100
		self.assertEquals(wigglytuff_instance.hp, 390)

		wigglytuff_instance.hp_ev = 252
		wigglytuff_instance.hp_iv = 31
		self.assertEquals(wigglytuff_instance.hp, 484)

	def test_other_stat_calculation(self):
		wigglytuff = Pokemon(bhp=140, batk=70, bdfn=45, bsatk=85, bsdfn=50, bspd=45)
		hardy = Nature(StatID.ATK, StatID.ATK)
		wigglytuff_instance = PokemonInstance(wigglytuff, nature=hardy)

		wigglytuff_instance.level = 50
		self.assertEquals(wigglytuff_instance.atk, 75)

		wigglytuff_instance.level = 100
		self.assertEquals(wigglytuff_instance.atk, 145)

		wigglytuff_instance.atk_ev = 252
		wigglytuff_instance.atk_iv = 31
		self.assertEquals(wigglytuff_instance.atk, 239)

	def test_other_stat_calculation_with_nature(self):
		wigglytuff = Pokemon(bhp=140, batk=70, bdfn=45, bsatk=85, bsdfn=50, bspd=45)
		adamant = Nature(StatID.ATK, StatID.SATK)
		wigglytuff_instance = PokemonInstance(wigglytuff, nature=adamant)

		wigglytuff_instance.level = 50
		self.assertEquals(wigglytuff_instance.atk, 82)

		wigglytuff_instance.level = 100
		self.assertEquals(wigglytuff_instance.atk, 159)

		wigglytuff_instance.atk_ev = 252
		wigglytuff_instance.atk_iv = 31
		self.assertEquals(wigglytuff_instance.atk, 262)

if __name__ == '__main__':
	unittest.main()
