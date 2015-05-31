import unittest

import fkmnkit
from fkmnkit.moves import verify_eq, eq_eval

class TestCustomFormulae(unittest.TestCase):
	def test_psywave(self):
		userlvl = 100

		formula = "tuple( max(1, (i + 50) * userlvl / 100) for i in range(101))"

		result = eq_eval(verify_eq(formula), {'userlvl': userlvl})

		self.assertEqual(len(result), 101)
		self.assertEqual(max(result), 150)
		self.assertEqual(min(result), 50)

	def test_set_damage(self):
		formula = "20"

		result = eq_eval(verify_eq(formula), {})

		self.assertEqual(result, 20)

if __name__ == '__main__':
	unittest.main()
