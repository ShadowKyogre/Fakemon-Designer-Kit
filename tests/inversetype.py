import unittest

import fkmnkit
from fkmnkit.poketypes import STANDARD_TYPES, PokeTypeSet
from fkmnkit.correctors import toInverseType, toInverseTypeSet, WonderType, WonderTypeSet

class TestInverseType(unittest.TestCase):
	def test_heatran(self):
		fire = toInverseType(STANDARD_TYPES['Fire'])
		steel = toInverseType(STANDARD_TYPES['Steel'])
		ground = toInverseType(STANDARD_TYPES['Ground'])
		heatran = PokeTypeSet((fire, steel))

		self.assertEqual(ground.effectiveness_against(heatran), 0.25)
		self.assertEqual(fire.effectiveness_against(heatran), 1)
		self.assertEqual(steel.effectiveness_against(heatran), 4)

	def test_mega_altaria(self):
		ice = toInverseType(STANDARD_TYPES['Ice'])
		dragon = toInverseType(STANDARD_TYPES['Dragon'])
		fairy = toInverseType(STANDARD_TYPES['Fairy'])
		mega_altaria = PokeTypeSet((dragon, fairy))

		self.assertEqual(fairy.effectiveness_against(mega_altaria), 0.5)
		self.assertEqual(dragon.effectiveness_against(mega_altaria), 1)
		self.assertEqual(ice.effectiveness_against(mega_altaria), 0.5)

	def test_shedinja(self):
		ghost = toInverseType(STANDARD_TYPES['Ghost'])
		bug = toInverseType(STANDARD_TYPES['Bug'])
		fire = toInverseType(STANDARD_TYPES['Fire'])
		steel = toInverseType(STANDARD_TYPES['Steel'])
		flying = toInverseType(STANDARD_TYPES['Flying'])
		fighting = toInverseType(STANDARD_TYPES['Fighting'])
		shedinja = PokeTypeSet((ghost, bug))
		flying_press = WonderTypeSet((fighting, flying))

		self.assertEqual(WonderType(fire).effectiveness_against(shedinja), 0)
		self.assertEqual(WonderType(ghost).effectiveness_against(shedinja), 0)
		self.assertEqual(WonderType(steel).effectiveness_against(shedinja), 0)
		self.assertEqual(WonderType(bug).effectiveness_against(shedinja), 2)
		self.assertEqual(flying_press.effectiveness_against(shedinja), 2)

	def test_hacked_spiritomb(self):
		ghost = toInverseType(STANDARD_TYPES['Ghost'])
		dark = toInverseType(STANDARD_TYPES['Dark'])
		fairy = toInverseType(STANDARD_TYPES['Fairy'])
		fire = toInverseType(STANDARD_TYPES['Fire'])

		spiritomb = PokeTypeSet((ghost, dark))
		self.assertEqual(WonderType(fairy).effectiveness_against(spiritomb), 0)
		self.assertEqual(WonderType(ghost).effectiveness_against(spiritomb), 0)
		self.assertEqual(WonderType(fire).effectiveness_against(spiritomb), 0)

if __name__ == '__main__':
	unittest.main()
