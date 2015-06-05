from enum import Enum
import ast
import builtins

AST_WHITELIST = (ast.Expression, ast.GeneratorExp, ast.Call, ast.Name, ast.Load,
                 ast.BinOp, ast.UnaryOp, ast.operator, ast.unaryop, ast.cmpop,
                 ast.Num, ast.Tuple, ast.Attribute, ast.comprehension, ast.Store, ast.IfExp, ast.Compare)
EVAL_SAFEDICT = {k: builtins.__dict__.get(k, None) for k in ('range', 'tuple', 'sum', 'max', 'min') }

def eq_eval(eq, lcl_vrs):
	use_this = {"__builtins__": EVAL_SAFEDICT}
	use_this.update(lcl_vrs)
	return eval(eq, use_this, {})

def verify_eq(user_eq):
	tree = ast.parse(user_eq, mode='eval')
	valid = all(isinstance(node, AST_WHITELIST) for node in ast.walk(tree))
	if valid:
		return compile(tree, filename='', mode='eval')
	else:
		raise ValueError("You can't use this for an equation!")

class MoveCategory(Enum):
	PHYSICAL = 0
	SPECIAL = 1
	STATUS = 2

class PokeMove:
	def __init__(self, label='', move_cat=MoveCategory.PHYSICAL, bp=0, dbp=0, cust_dmg=None, accuracy=100, efftypes=None, stabtype=None):
		self.label = label
		self.move_cat = move_cat
		self.bp_formula = bp
		self.dbp = dbp
		self.accuracy = accuracy
		self.efftypes = efftypes
		self.stabtype = stabtype
		self.custom_damage_formula = cust_dmg

	@property
	def custom_damage_formula(self):
		return self._cdf

	@custom_damage_formula.setter
	def custom_damage_formula(self, cdf)
		if isinstance(cdf, str):
			self._cdf = cdf
			try:
				self._cdf_code = verify_eq(cdf)
			except ValueError as e:
				print("Invalid formula, preserving formula for editing")
				self._cdf_code = None
		elif isinstance(cdf, int):
			self._cdf = cdf
			self._cdf_code = None
		elif cdf is None:
			self._cdf None None
			self._cdf_code = None
		else:
			raise ValueError("Custom damage is neither a formula string nor a function!")

	@property
	def bp_formula(self):
		return self._bp

	@bp_formula.setter
	def bp_formula(self, bp):
		if isinstance(bp, str):
			self._bp = bp
			try:
				self._bp_code = verify_eq(bp)
			except ValueError as e:
				print("Invalid formula, preserving formula for editing")
				self._bp_code = None
		elif isinstance(bp, int):
			self._bp = bp
			self._bp_code = None
		else:
			raise ValueError("BP is neither a formula string nor a function!")

	def bp(self, user, *targets):
		if isinstance(self._bp, str):
			if self._bp_code is not None:
				return eq_eval(self._bp_code, {'user':user, 'targets': targets})
			else:
				return 0
		elif isinstance(self._bp, int):
			return self._bp

	def custom_damage(self, user, *targets):
		if isinstance(self._cdf, str):
			return eq_eval(self._cdf_code, {'user':user, 'targets': targets})
		elif isinstance(self._cdf, int):
			return self._cdf

	def applicable_stab(self, pkmn):
		#need stabtype because pokes like Hawlucha don't get double STAB from dual type
		if self.stabtype in pkmn.types:
			if len(pkmn.types) > 1:
				return 1.25
			else:
				return 1.5
		else:
			return 1
