import unittest

from poketypes import STANDARD_TYPES, PokeTypeSet
from correctors import WonderType

class TestWonderGuard(unittest.TestCase):
	def test_shedinja(self):
		ghost = STANDARD_TYPES['Ghost']
		bug = STANDARD_TYPES['Bug']
		fire = STANDARD_TYPES['Fire']
		steel = STANDARD_TYPES['Steel']
		shedinja = PokeTypeSet((ghost, bug))

		self.assertEqual(WonderType(fire) * shedinja, 2)
		self.assertEqual(WonderType(ghost) * shedinja, 2)
		self.assertEqual(WonderType(steel) * shedinja, 0)
		self.assertEqual(WonderType(bug) * shedinja, 0)

if __name__ == '__main__':
	unittest.main()
