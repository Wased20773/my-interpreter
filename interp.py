from dataclasses import dataclass
from midiutil import MIDIFile

type Expr = Add | Sub | Mul | Div | Neg | Lit | And | Or | Not | Let | Name | Eq | Neq | Lt | LorE | Gt | GorE | If

# Added = ✅
# ------ Core Language 1 ----- #
# Arithmitic
#   - Lit(int) ✅
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
#   - If ✅
#   - more? (might be discussed with professor in lecture)

# ------ Core Language 7 ----- #
#   - Note ✅
#   - Tune ✅
#   - ConcatTunes ✅
#   - Transpose

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
@dataclass
class Note:
    pitch: str # "C", "D", "E", "F", "G", "A", "B" or "R" for rest
    duration: Expr # in seconds (evaluated to an integer)

    def __str__(self):
        return f"Note(Pitch: {self.pitch}, Duration: {self.duration})"

@dataclass
class Tune:
    notes: list[Note]

    def __str__(self):
        return f" Tune[{', '.join(str(note) for note in self.notes)}]"

@dataclass
class ConcatTunes:
    left: Tune
    right: Tune

    def __str__(self):
        return f"ConcatTunes({self.left}, {self.right})"

@dataclass
class Transpose:
    tune: Tune
    steps: int

    def __str__(self):
        return f"Transpose({self.tune}, {self.steps})"

NOTE_TO_MIDI = {
    "C": 60, "C#": 61,
    "D": 62, "D#": 63,
    "E": 64,
    "F": 65, "F#": 66,
    "G": 67, "G#": 68,
    "A": 69, "A#": 70,
    "B": 71,
    "R": 0,  # Rest
}
MIDI_TO_NOTE = {
    60: "C", 61: "C#",
    62: "D", 63: "D#",
    64: "E", 
    65: "F", 66: "F#", 
    67: "G", 68: "G#",
    69: "A", 70: "A#",
    71: "B",
    0:  "R",  # Rest (no pitch)
}

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

def transpose_note(tune: Tune, steps: int) -> Tune:
    if not isinstance(tune, Tune):
        raise EvalError("Transpose note to be type Note")
    
    notes = []

    # Go through the all notes in a tune
    for note in tune.notes:
        if note.pitch == "R":
            notes.append(note)
            continue

        # Get the midi value of the pitch
        midi = NOTE_TO_MIDI.get(note.pitch) # Might be an issue
        if midi == None:
            raise EvalError(f"Could not translate pitch: {note.pitch}")
        
        # Calcualte transposed midi value with steps
        transpose_midi = midi + steps
        
        if transpose_midi < NOTE_TO_MIDI["C"]:
            difference = NOTE_TO_MIDI["C"] - transpose_midi
            transpose_midi = (NOTE_TO_MIDI["B"] - difference) + 1
        elif transpose_midi > NOTE_TO_MIDI["B"]:
            difference = transpose_midi - NOTE_TO_MIDI["B"]
            transpose_midi = (difference + NOTE_TO_MIDI["C"]) - 1

        # Get the new pitch from transposed midi value
        new_pitch = MIDI_TO_NOTE[transpose_midi]
        notes.append(Note(new_pitch, note.duration))

    return Tune(notes)


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
            elif not isinstance(left, int) or not isinstance(right, int):
                raise EvalError("addition operator requires integer operands")
            return left + right
        
        case Sub(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if isinstance(left, bool) or isinstance(right, bool):
                raise EvalError("cannot subtract boolean values")
            elif not isinstance(left, int) or not isinstance(right, int):
                raise EvalError("subtraction operator requires integer operands")
            return left - right
        
        case Mul(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if isinstance(left, bool) or isinstance(right, bool):
                raise EvalError("cannot multiply boolean values")
            elif not isinstance(left, int) or not isinstance(right, int):
                raise EvalError("multiplication operator requires integer operands")
            return left * right
        
        case Div(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if isinstance(left, bool) or isinstance(right, bool):
                raise EvalError("cannot divide boolean values")
            elif not isinstance(left, int) or not isinstance(right, int):
                raise EvalError("division operator requires integer operands")
            if (right == 0):
                raise EvalError("division by zero")
            return left // right
        
        case Neg(e):
            value = evalInEnv(env, e)
            if isinstance(value, bool):
                raise EvalError("cannot negate boolean values")
            elif not isinstance(value, int):
                raise EvalError("negation operator requires integer operands")
            return -value
        
        case And(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if not isinstance(left, bool) or not isinstance(right, bool):
                raise EvalError("And operator requires boolean operands")
            return left and right
        
        case Or(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if not isinstance(left, bool) or not isinstance(right, bool):
                raise EvalError("Or operator requires boolean operands")
            return left or right

        
        case Not(e):
            value = evalInEnv(env, e)
            if not isinstance(value, bool):
                raise EvalError("Not operator requires boolean operands")
            return not value
        
        case Name(name):
            value = lookupEnv(name, env)
            if value is None:
                raise EvalError(f"unbound Name: {name}")
            return value
        
        case Let(name, defn, body):
            if name == "":
                raise EvalError("Name cannot be empty")
            if not isinstance(name, str):
                raise EvalError("Name must be a string")

            # Get expression of name
            new_defn = evalInEnv(env, defn)
            # Extend env with name
            newEnv = extendEnv(name, new_defn, env)
            return evalInEnv(newEnv, body)
        
        case Eq(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            # check if left and right are the same type
            # while also excepting mixed types, like int and bool
            if type(left) != type(right):
                raise EvalError("cannot compare different types")
            if isinstance(left, bool) and isinstance(right, bool):
                return left == right
            elif isinstance(left, int) and isinstance(right, int):
                return left == right
            else:
                raise EvalError("Must compare using int, or bool types")
            
        case Neq(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            # check if left and right are the same type
            # while also excepting mixed types, like int and bool
            if type(left) != type(right):
                raise EvalError("cannot compare different types")
            if isinstance(left, bool) and isinstance(right, bool):
                return left != right
            elif isinstance(left, int) and isinstance(right, int):
                return left != right
            else:
                raise EvalError("Must compare using int, or bool types")
        
        case Lt(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if isinstance(left, int) and isinstance(right, int):
                return left < right
            else:
                raise EvalError("operand must be integer")
            
        case LorE(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if isinstance(left, int) and isinstance(right, int):
                return left <= right
            else:
                raise EvalError("operand must be integer")
            
        case Gt(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if isinstance(left, int) and isinstance(right, int):
                return left > right
            else:
                raise EvalError("operand must be integer")
            
            
        case GorE(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if isinstance(left, int) and isinstance(right, int):
                return left >= right
            else:
                raise EvalError("operand must be integer")
            
        case If(b, t, e):
            cond = evalInEnv(env, b)
            if not isinstance(cond, bool):
                raise EvalError("If condition must be boolean")
            
            
            if cond: # if condition is true
                then_branch = evalInEnv(env, t)
                if not isinstance(then_branch, (int, bool)):
                    raise EvalError("If then must be int or bool")
                return then_branch
            else:   # condition is false
                else_branch = evalInEnv(env, e)
                if not isinstance(else_branch, (int, bool)):
                    raise EvalError("If else must be int or bool")
                return else_branch

        # ----- Domain-specific extension (Tunes) ----- #
        case Note(name, d):
            if not isinstance(name, str):
                raise EvalError("Note name must be a string")
            if name not in NOTE_TO_MIDI:
                raise EvalError(f"Invalid note name: {name}. Must be one of {list(NOTE_TO_MIDI.keys())}")

            duration = evalInEnv(env, d)

            # Check for duration
            if not isinstance(duration, int) or duration <= 0:
                raise EvalError("Note duration must be a positive integer")
            
            return Note(name, duration)
        
        case Tune(n):
            if not isinstance(n, list):
                raise EvalError("Seq must be a list of notes")
            
            result = []
            # Check if all elements in the list are Note objects
            for note in n:
                if not isinstance(note, Note):
                    raise EvalError("Seq must contain only Note objects")
                note_value = evalInEnv(env, note)
                result.append(note_value)
            
            return Tune(result)

        case ConcatTunes(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)

            if not isinstance(left, Tune) or not isinstance(right, Tune):
                raise EvalError("ConcatTunes must be two Tunes")

            return Tune(left.notes + right.notes)

        case Transpose(t, s):
            if not isinstance(t, Tune):
                return EvalError("Transpose can only tune up or down Tunes")
            
            return transpose_note(t, s)

        case _:
            raise EvalError(f"unknown expression: {expr}")


def run(expr: Expr) -> None:
    print(f"running: {expr}") # Might remove
    try:
        result = eval(expr)

        print(f"result: {result}")
    except EvalError as err:
        print(err)

d : Expr = Tune([Note("E", Lit(4)), Note("D", Lit(4)), Note("E", Lit(4))])
e : Expr = Tune([Note("F", Add(Lit(4), Lit(2)))])
f : Expr = Tune([Note("R", If(Eq(Lit(1), Lit(1)), Lit(4), Lit(2)))])
g : Expr = ConcatTunes(e, f)
h : Expr = Transpose(f, 5)
i : Expr = Transpose(d, -5)
j : Expr = Transpose(e, 10)

run(d)
run(e)
run(f)
run(g)
run(h)
run(i)
run(j)