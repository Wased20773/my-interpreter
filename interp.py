from dataclasses import dataclass

type Expr = Add | Sub | Mul | Div | Neg | Lit | And | Or | Not | Let | Name | Eq | Neq | Lt | LorE | Gt | GorE | If

# Added = ✅
# ------ Core Language 1 -----
# Arithmitic
#   - Lit(int) ✅
#   - Add ✅
#   - Sub ✅
#   - Mul ✅
#   - Div ✅
#   - Neg ✅

# ------ Core Language 2 -----
# boolean
#   - Lit(bool)
#   - And ✅
#   - Or ✅
#   - Not ✅

# ------ Core Language 3 -----
# binding/variables
#   - Let ✅
#   - Name ✅

# ------ Core Language 4 -----
# equality comparison
#   - Eq ✅
#   - Neq ✅

# ------ Core Language 5 -----
# relation comparison
#   - Lt ✅
#   - LorE ✅
#   - Gt ✅
#   - GorE ✅

# ------ Core Language 6 -----
# conditional
#   - If
#   - more? (might be discussed with professor in lecture)

# ------ Core Language 7 -----
# Domain-specific extension (Tunes)

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
    value: int | bool # needs bool too
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

# ----- Domain-specific extension (Tunes) -----

# Dont focus on this yet
@dataclass
class Note:
    pass

def eval(expr: Expr) -> Expr:
    match expr:
        case Add(l, r):
            return eval(l) + eval(r)
        case Sub(l, r):
            return eval(l) - eval(r)
        case Mul(l, r):
            return eval(l) * eval(r)
        case Div(l, r):
            return eval(l) / eval(r)
        case Neg(e):
            return -eval(e)
        case Lit(v):
            return v
        case And(l, r):
            return eval(l) and eval(r)
        case Or(l, r):
            return eval(l) or eval(r)
        case Not(e):
            return not eval(e)
