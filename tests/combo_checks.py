import unittest

import fkmnkit
from fkmnkit.poketypes import STANDARD_TYPES, PokeTypeSet

class TestComboChecks(unittest.TestCase):
	def test_heatran(self):
		fire = STANDARD_TYPES['Fire']
		steel = STANDARD_TYPES['Steel']
		ground = STANDARD_TYPES['Ground']
		heatran = PokeTypeSet((fire, steel))

		self.assertEqual(ground.effectiveness_against(heatran), 4)
		self.assertEqual(fire.effectiveness_against(heatran), 1)
		self.assertEqual(steel.effectiveness_against(heatran), 0.25)

	def test_mega_altaria(self):
		ice = STANDARD_TYPES['Ice']
		dragon = STANDARD_TYPES['Dragon']
		fairy = STANDARD_TYPES['Fairy']
		mega_altaria = PokeTypeSet((dragon, fairy))

		self.assertEqual(fairy.effectiveness_against(mega_altaria), 2)
		self.assertEqual(dragon.effectiveness_against(mega_altaria), 0)
		self.assertEqual(ice.effectiveness_against(mega_altaria), 2)
if __name__ == '__main__':
	unittest.main()
