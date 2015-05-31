import unittest

import fkmnkit
from fkmnkit.creatures import Pokemon

class TestPokemonCreation(unittest.TestCase):
	def test_bst_validation(self):
		with self.assertRaises(ValueError):
			Pokemon(bhp=300)

		actual_pokemon = Pokemon(bhp=200)
		self.assertEquals(actual_pokemon.bhp, 200)

if __name__ == '__main__':
	unittest.main()
