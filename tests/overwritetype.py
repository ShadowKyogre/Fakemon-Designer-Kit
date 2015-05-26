import unittest

import fkmnkit
from fkmnkit.poketypes import STANDARD_TYPES, PokeTypeSet
from fkmnkit.correctors import OverwriteType

class TestFreezeDried(unittest.TestCase):
	def test_blastoise(self):
		water = STANDARD_TYPES['Water']
		ice = STANDARD_TYPES['Ice']
		blastoise = PokeTypeSet((water,))

		self.assertEqual(OverwriteType(ice, orw=set((water,))).effectiveness_against(blastoise), 2)
		self.assertEqual(water.effectiveness_against(blastoise), 0.5)

	def test_miracle_matter(self):
		fire = STANDARD_TYPES['Fire']
		water = STANDARD_TYPES['Water']
		ice = STANDARD_TYPES['Ice']

		miracle_matter = PokeTypeSet((fire,))
		self.assertEqual(OverwriteType(fire, orw=set((fire,))).effectiveness_against(miracle_matter), 2)
		self.assertEqual(ice.effectiveness_against(miracle_matter), 0.5)
		self.assertEqual(water.effectiveness_against(miracle_matter), 2)
		self.assertEqual(OverwriteType(ice, ori=set((fire,))).effectiveness_against(miracle_matter), 0)
		self.assertEqual(OverwriteType(water, ori=set((fire,))).effectiveness_against(miracle_matter), 0)

	def test_toxicroak(self):
		fire = STANDARD_TYPES['Fire']
		poison = STANDARD_TYPES['Poison']
		fighting = STANDARD_TYPES['Fighting']
		psychic = STANDARD_TYPES['Psychic']
		water = STANDARD_TYPES['Water']

		toxicroak = PokeTypeSet((poison, fighting))
		self.assertEqual(fire.effectiveness_against(toxicroak), 1)
		self.assertEqual(poison.effectiveness_against(toxicroak), 0.5)
		self.assertEqual(fighting.effectiveness_against(toxicroak), 0.5)
		self.assertEqual(psychic.effectiveness_against(toxicroak), 4)

		self.assertEqual(OverwriteType(fire, orw=set((poison,))).effectiveness_against(toxicroak), 2)
		self.assertEqual(OverwriteType(water, ori=set((poison,))).effectiveness_against(toxicroak), 0)



if __name__ == '__main__':
	unittest.main()
