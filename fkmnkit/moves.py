from enum import Enum
import ast
import builtins

AST_WHITELIST = (ast.Expression, ast.GeneratorExp, ast.Call, ast.Name, ast.Load,
                 ast.BinOp, ast.UnaryOp, ast.operator, ast.unaryop, ast.cmpop,
                 ast.Num, ast.Tuple, ast.Attribute, ast.comprehension, ast.Store)
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
	def __init__(self, label='', move_cat=MoveCategory.PHYSICAL, bp=0, dbp=0, accuracy=100, efftypes=None, stabtype=None):
		self.label = label
		self.move_cat = move_cat
		self.bp = bp
		self.dbp = dbp
		self.accuracy = accuracy
		self.efftypes = efftypes
		self.stabtype = stabtype

	def applicable_stab(self, pkmn):
		#need stabtype because pokes like Hawlucha don't get double STAB from dual type
		if self.stabtype in pkmn.types:
			if len(pkmn.types) > 1:
				return 1.25
			else:
				return 1.5
		else:
			return 1
