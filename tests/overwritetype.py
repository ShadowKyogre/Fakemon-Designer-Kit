import unittest

import fkmnkit
from fkmnkit.poketypes import STANDARD_TYPES, PokeTypeSet
from fkmnkit.correctors import OverwriteType

class TestFreezeDried(unittest.TestCase):
	def test_blastoise(self):
		water = STANDARD_TYPES['Water']
		ice = STANDARD_TYPES['Ice']
		blastoise = PokeTypeSet((water,))

		self.assertEqual(OverwriteType(ice, orw=set((water,))) * blastoise, 2)
		self.assertEqual(water * blastoise, 0.5)

	def test_miracle_matter(self):
		fire = STANDARD_TYPES['Fire']
		water = STANDARD_TYPES['Water']
		ice = STANDARD_TYPES['Ice']

		miracle_matter = PokeTypeSet((fire,))
		self.assertEqual(OverwriteType(fire, orw=set((fire,))) * miracle_matter, 2)
		self.assertEqual(ice * miracle_matter, 0.5)
		self.assertEqual(water * miracle_matter, 2)
		self.assertEqual(OverwriteType(ice, ori=set((fire,))) * miracle_matter, 0)
		self.assertEqual(OverwriteType(water, ori=set((fire,))) * miracle_matter, 0)

	def test_toxicroak(self):
		fire = STANDARD_TYPES['Fire']
		poison = STANDARD_TYPES['Poison']
		fighting = STANDARD_TYPES['Fighting']
		psychic = STANDARD_TYPES['Psychic']
		water = STANDARD_TYPES['Water']

		toxicroak = PokeTypeSet((poison, fighting))
		self.assertEqual(fire * toxicroak, 1)
		self.assertEqual(poison * toxicroak, 0.5)
		self.assertEqual(fighting * toxicroak, 0.5)
		self.assertEqual(psychic * toxicroak, 4)

		self.assertEqual(OverwriteType(fire, orw=set((poison,))) * toxicroak, 2)
		self.assertEqual(OverwriteType(water, ori=set((poison,))) * toxicroak, 0)



if __name__ == '__main__':
	unittest.main()
