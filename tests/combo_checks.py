import unittest

import fkmnkit
from fkmnkit.poketypes import STANDARD_TYPES, PokeTypeSet

class TestComboChecks(unittest.TestCase):
	def test_heatran(self):
		fire = STANDARD_TYPES['Fire']
		steel = STANDARD_TYPES['Steel']
		ground = STANDARD_TYPES['Ground']
		heatran = PokeTypeSet((fire, steel))

		self.assertEqual(ground * heatran, 4)
		self.assertEqual(fire * heatran, 1)
		self.assertEqual(steel * heatran, 0.25)

	def test_mega_altaria(self):
		ice = STANDARD_TYPES['Ice']
		dragon = STANDARD_TYPES['Dragon']
		fairy = STANDARD_TYPES['Fairy']
		mega_altaria = PokeTypeSet((dragon, fairy))

		self.assertEqual(fairy * mega_altaria, 2)
		self.assertEqual(dragon * mega_altaria, 0)
		self.assertEqual(ice * mega_altaria, 2)
if __name__ == '__main__':
	unittest.main()
