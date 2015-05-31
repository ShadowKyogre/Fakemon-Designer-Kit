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
	
	def test_low_kick(self):
		formula = "120 if w>=200 else 100 if w>=100 else 80 if w>=50 else 60 if w>=25 else 40 if w>=10 else 20"
		self.assertEqual(eq_eval(verify_eq(formula), {'w': 200}), 120)
		self.assertEqual(eq_eval(verify_eq(formula), {'w': 100}), 100)
		self.assertEqual(eq_eval(verify_eq(formula), {'w': 50}),   80)
		self.assertEqual(eq_eval(verify_eq(formula), {'w': 25}),   60)
		self.assertEqual(eq_eval(verify_eq(formula), {'w': 10}),   40)
		self.assertEqual(eq_eval(verify_eq(formula), {'w': 5}),    20)


if __name__ == '__main__':
	unittest.main()
