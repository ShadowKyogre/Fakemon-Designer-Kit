import unittest

import fkmnkit
from fkmnkit.poketypes import STANDARD_TYPES, PokeTypeSet
from fkmnkit.correctors import WonderType

class TestWonderGuard(unittest.TestCase):
	def test_shedinja(self):
		ghost = STANDARD_TYPES['Ghost']
		bug = STANDARD_TYPES['Bug']
		fire = STANDARD_TYPES['Fire']
		steel = STANDARD_TYPES['Steel']
		flying = STANDARD_TYPES['Flying']
		fighting = STANDARD_TYPES['Fighting']
		shedinja = PokeTypeSet((ghost, bug))
		flying_press = PokeTypeSet((WonderType(fighting), WonderType(flying)))

		self.assertEqual(WonderType(fire) * shedinja, 2)
		self.assertEqual(WonderType(ghost) * shedinja, 2)
		self.assertEqual(WonderType(steel) * shedinja, 0)
		self.assertEqual(WonderType(bug) * shedinja, 0)
		self.assertEqual(flying_press * shedinja, 0)

	def test_hacked_spiritomb(self):
		ghost = STANDARD_TYPES['Ghost']
		dark = STANDARD_TYPES['Dark']
		fairy = STANDARD_TYPES['Fairy']
		fire = STANDARD_TYPES['Fire']

		spiritomb = PokeTypeSet((ghost, dark))
		self.assertEqual(WonderType(fairy) * spiritomb, 2)
		self.assertEqual(WonderType(ghost) * spiritomb, 0)
		self.assertEqual(WonderType(fire) * spiritomb, 0)

if __name__ == '__main__':
	unittest.main()
