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


# ----- Expressions ----- #
a: Expr = Add(Add(Lit(5), Lit(2)), Lit(8))
print(a)
# ((5 + 2) + 8)

b: Expr = Add(Add(Lit(3.8), Lit(0.2)), Lit(1))
print(b)
# (4.8 + 0.2)

c: Expr = Sub(Lit(5), Lit(1))
print(c)
# (5 - 1)

d: Expr = Mul(Add(Add(Lit(4), Lit(2)), Neg(Lit(2))), Lit(2))
print(d)
# (((4 + 2) + (-2)) * 2)

e: Expr = Div(Add(Lit(4), Lit(2)), Lit(2))
print(e)
# ((4 + 2) / 2)

f: Expr = Div(Lit(6), Lit(0))
print(f)
# (6 / 0)

g: Expr = Div(Lit(0), Lit(6))
print(g)
# (0 / 6)

h: Expr = Div(Lit(5), Lit(2))
print(h)
# (5 / 2)

i: Expr = Neg(Add(Lit(5), Lit(2)))
print(i)
# (5 / 2)

j: Expr = Neg(Lit(10))
print(j)
# (-10)

k: Expr = And(Lit(True), Lit(5))
print(k)
# (True and 5)

l: Expr = Add(Lit(True), Lit(1))
print(l)
# (True + 1)

m: Expr = Not(Lit(5))
print(m)
# (not 5)

n: Expr = Neg(Lit(False))
print(n)
# (not 5)

o: Expr = Let("x", Add(Lit(1), Lit(2)), Sub(Name("x"), Lit(3)))
print(o)
# (Let x = (1 + 2) in (x - 3))

p: Expr = Let("x", Lit(5), (Let("y", Lit(2), Add(Name("x"), Name("y")))))
print(p)
# (Let x = 5 in (Let y = 2 in (x + y)))

q: Expr = Let("x", Lit(5), (Let("y", Lit(2), (Let("x", Lit(2), Add(Name("x"), Name("y")))))))
print(q)
# (let x = 5 in (let y = 2 in (let x = 2 in (x + y))))

# r: Expr = 

# s: Expr = 

# t: Expr = 

# u: Expr = 

# v: Expr = 

# w: Expr = 

# x: Expr = 

# y: Expr = 

# z: Expr = 

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
            if not isinstance(evalInEnv(env, e), bool):
                raise EvalError("not operator requires boolean operands")
            elif isinstance(evalInEnv(env, e), bool):
                return False
            return True
        
        case Name(name):
            value = lookupEnv(name, env)
            if value is None:
                raise EvalError(f"unbound name: {name}")
            return value
        
        case Let(name, defn, body):
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

run(a) # 15
run(b) # 5.0
run(c) # 4
run(d) # 8
run(e) # 3.0
run(f) # division by zero
run(g) # 0.0
run(h) # 2.5
run(i) # -7
run(j) # -10
run(k) # and operator requires boolean operands
run(l) # cannot add boolean values
run(m) # not operator requires boolean operands
run(n) # cannot negate boolean values
run(o) # 0
run(p) # 7
run(q) # 4