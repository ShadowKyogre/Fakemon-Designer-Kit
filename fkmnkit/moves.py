from enum import Enum
import ast

AST_WHITELIST = (ast.Expression, ast.Call, ast.Name, ast.Load,
                 ast.BinOp, ast.UnaryOp, ast.operator, ast.unaryop, ast.cmpop,
                 ast.Num, ast.Tuple, ast.Attribute)
EVAL_SAFEDICT = {k:locals().get(k, None) for k in ('range', 'tuple') }

def eq_eval(eq, lcl_vrs):
	lcl_vrs_cpy = lcl_vrs.copy()
	lcl_vrs_cpy.update(EVAL_SAFEDICT)
	return eval(eq, {"__builtins__": None})

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
	def __init__(self, label='', move_cat=MoveCategory.PHYSICAL, bp="0", accuracy=100, efftype=None, stabtype=None):
		pass

	def applicable_stab(self, pkmn):
		#need stabtype because pokes like Hawlucha don't get double STAB from dual type
		if self.stabtype in pkmn.types:
			if len(pkmn.types) > 1:
				return 1.25
			else:
				return 1.5
		else:
			return 1
