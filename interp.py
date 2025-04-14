from dataclasses import dataclass

type Expr = Add | Sub | Mul | Div | Neg | Lit | And | Or | Not | Let | Name | Eq | Neq | Lt | LorE | Gt | GorE | If

# Added = ✅
# ------ Core Language 1 ----- #
# Arithmitic
#   - Lit(int) ✅
#   - Lit(float) ✅
#   - Add ✅
#   - Sub ✅
#   - Mul ✅
#   - Div ✅
#   - Neg ✅

# ------ Core Language 2 ----- #
# boolean
#   - Lit(bool)
#   - And ✅
#   - Or ✅
#   - Not ✅

# ------ Core Language 3 ----- #
# binding/variables
#   - Let ✅
#   - Name ✅

# ------ Core Language 4 ----- #
# equality comparison
#   - Eq ✅
#   - Neq ✅

# ------ Core Language 5 ----- #
# relation comparison
#   - Lt ✅
#   - LorE ✅
#   - Gt ✅
#   - GorE ✅

# ------ Core Language 6 ----- #
# conditional
#   - If
#   - more? (might be discussed with professor in lecture)

# ------ Core Language 7 ----- #
# Domain-specific extension (Tunes)
'''

'''

@dataclass
class Add:
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} + {self.right})"

@dataclass
class Sub:
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} - {self.right})"

@dataclass
class Mul:
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} * {self.right})"

@dataclass
class Div:
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} / {self.right})"

@dataclass
class Neg:
    expr: Expr
    def __str__(self):
        return f"(-{self.expr})"
    
@dataclass
class Lit:
    value: int | bool
    def __str__(self):
        return str(self.value)

@dataclass
class And:
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} and {self.right})"
    
@dataclass
class Or:
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} or {self.right})"
    
@dataclass
class Not:
    subexpr: Expr
    def __str__(self):
        return f"(not {self.subexpr})"
    
@dataclass
class Let:
    varname: str
    defnexpr: Expr
    bodyexpr: Expr
    def __str__(self):
        return f"(let {self.varname} = {self.defnexpr} in {self.bodyexpr})"
    
@dataclass
class Name:
    varname: str
    def __str__(self):
        return self.varname

# Equal to
@dataclass
class Eq:
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} == {self.right})"
    
# Not equal to
@dataclass
class Neq:
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} != {self.right})"
    
# Less than
@dataclass
class Lt:
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} < {self.right})"
    
# Less than or Equal to
@dataclass
class LorE:
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} <= {self.right})"
    
# Greater than
@dataclass
class Gt:
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} > {self.right})"

# Greater than or Equal to
@dataclass
class GorE:
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} >= {self.right})"
    

@dataclass
class If:
    cond: Expr
    then: Expr
    else_: Expr
    def __str__(self):
        return f"(if {self.cond} then {self.then} else {self.else_})"

# ----- Domain-specific extension (Tunes) ----- #

# Dont focus on this yet
@dataclass
class Note:
    pass

# ----- Environment ----- #

type Binding[V] = tuple[str, V]  # this tuple type is always a pair
type Env[V] = tuple[Binding[V], ...]  # this tuple type has arbitrary length


from typing import Any
emptyEnv: Env[Any] = ()  # the empty environment has no bindings


def extendEnv[V](name: str, value: V, env: Env[V]) -> Env[V]:
    '''Extend the environment env with a new binding of name to value'''
    return ((name, value),) + env  # add a new binding to the front of the environment


def lookupEnv[V](name: str, env: Env[V]) -> V | None:
    '''Return the value bound to name in env, or None if name is not bound'''
    match env:
        case ((n, v), *rest):
            if n == name:
                return v
            else:
                return lookupEnv(name, rest)
        case _:
            return None

class EvalError(Exception):
    pass


def eval(expr: Expr) -> Expr:
    return evalInEnv(emptyEnv, expr)


def evalInEnv(env: Env[Expr], expr: Expr) -> Expr:
    match expr:
        case Lit(v):
            return v
        
        case Add(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if isinstance(left, bool) or isinstance(right, bool):
                raise EvalError("cannot add boolean values")
            elif not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise EvalError("addition operator requires numeric operands")
            return left + right
        
        case Sub(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if isinstance(left, bool) or isinstance(right, bool):
                raise EvalError("cannot subtract boolean values")
            elif not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise EvalError("subtraction operator requires numeric operands")
            return left - right
        
        case Mul(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if isinstance(left, bool) or isinstance(right, bool):
                raise EvalError("cannot multiply boolean values")
            elif not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise EvalError("multiplication operator requires numeric operands")
            return left * right
        
        case Div(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if isinstance(left, bool) or isinstance(right, bool):
                raise EvalError("cannot divide boolean values")
            elif not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise EvalError("division operator requires numeric operands")
            if (right == 0):
                raise EvalError("division by zero")
            return left / right
        
        case Neg(e):
            value = evalInEnv(env, e)
            if isinstance(value, bool):
                raise EvalError("cannot negate boolean values")
            elif not isinstance(value, (int, float)):
                raise EvalError("negation operator requires numeric operands")
            return -value
        
        case And(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if not isinstance(left, bool) or not isinstance(right, bool):
                raise EvalError("and operator requires boolean operands")
            elif isinstance(left, bool) and isinstance(right, bool):
                return left and right
            return False
        
        case Or(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if not isinstance(left, bool) or not isinstance(right, bool):
                raise EvalError("or operator requires boolean operands")
            elif isinstance(left, bool) and isinstance(right, bool):
                return left or right
            return False
        
        case Not(e):
            value = evalInEnv(env, e)
            if not isinstance(value, bool):
                raise EvalError("not operator requires boolean operands")
            return not value
        
        case Name(name):
            value = lookupEnv(name, env)
            if value is None:
                raise EvalError(f"unbound name: {name}")
            return value
        
        case Let(name, defn, body):
            if name == "":
                raise EvalError("name cannot be empty")

            # Get expression of name
            new_defn = evalInEnv(env, defn)
            # Extend env with name
            newEnv = extendEnv(name, new_defn, env)
            return evalInEnv(newEnv, body)


def run(expr: Expr) -> None:
    print(f"running: {expr}") # Might remove
    try:
        i = eval(expr)
        if isinstance(i, float) and i.is_integer(): # Convert float to int if it is something like 3.0
            i = int(i)

        print(f"result: {i}")
    except EvalError as err:
        print(err)
