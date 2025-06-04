# This is Milestone 1 of my interpreter project that includes 
# Basic core languages, seen below, and a domain-specific extension
# for music, Tune. You'll need to install MIDIUtil to run this code
# using `pip install MIDIUtil` (Version 1.2.1).
'''

# ----- Brief description of the Domain-specific extension ----- #

The Domain-specific extension that will be used is Tune, which will contain
a list of Note types. It is intended for only Tune's to play music, while Note's
will only be displayed by evaluation. An expression of type Tune is intended
to be only a single Tune, no nested Tunes. Each Note is intended to use some of
the basic core languages, such as using + to add to the Note's duration.

The operators that are part of this extension is to provide for more flexibility.
ConcatTunes will, in the name, concate tunes. Transpose will increase, or decrease
the note of every Note in a single Tune by an according value (half-steps).

'''
from dataclasses import dataclass
from midiutil import MIDIFile
import os

type Expr = Add | Sub | Mul | Div | Neg | Lit \
    | And | Or | Not \
    | Let | Letfun | If | Assign | Seq | Show | Name | App \
    | Eq | Neq | Lt | LorE | Gt | GorE \
    | Note | Tune | ConcatTunes | Transpose | Repeat | Volume


# Added = ✅
# ----- Milestone 1 Requirements ----- #
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
#   - Lit(bool) ✅
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

# ------ Core Language 7 ----- #
#   - Note ✅
#   - Tune ✅
#   - ConcatTunes ✅
#   - Transpose ✅

# ----- Milestone 2 Requirements ----- #
# ----- Core language to add ----- #
#   - Ifnz ✅
#   - Letfun ✅
#   - App ✅
# ----- Milestone 3 Requirements ----- #
#   - Create Mutability
#       - Name ✅
#       - Let ✅
#       - Letfun ✅
#       - App ✅
#       - Assign ✅
#   - Create Seq ✅
#   - new operations
#       - Read ✅
#       - Show ✅
#   - new DSL operators
#       - Repeat ✅
#       - Volume ✅
#       - Track ✅

@dataclass
class Add():
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} + {self.right})"

@dataclass
class Sub():
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} - {self.right})"

@dataclass
class Mul():
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} * {self.right})"

@dataclass
class Div():
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} / {self.right})"

@dataclass
class Neg():
    expr: Expr
    def __str__(self):
        return f"(-{self.expr})"
    
@dataclass
class Lit():
    value: int | bool
    def __str__(self):
        return str(self.value)

@dataclass
class And():
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} and {self.right})"
    
@dataclass
class Or():
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} or {self.right})"
    
@dataclass
class Not():
    subexpr: Expr
    def __str__(self):
        return f"(not {self.subexpr})"
    
@dataclass
class Let():
    varname: str
    defnexpr: Expr
    bodyexpr: Expr
    def __str__(self):
        return f"(let {self.varname} = {self.defnexpr} in {self.bodyexpr})"
    
@dataclass
class Name():
    varname: str
    def __str__(self):
        return self.varname

# Equal to
@dataclass
class Eq():
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} == {self.right})"
    
# Not equal to
@dataclass
class Neq():
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} != {self.right})"
    
# Less than
@dataclass
class Lt():
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} < {self.right})"
    
# Less than or Equal to
@dataclass
class LorE():
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} <= {self.right})"
    
# Greater than
@dataclass
class Gt():
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} > {self.right})"

# Greater than or Equal to
@dataclass
class GorE():
    left: Expr
    right: Expr
    def __str__(self):
        return f"({self.left} >= {self.right})"
    

@dataclass
class If():
    cond: Expr
    then: Expr
    else_: Expr
    def __str__(self):
        return f"(if {self.cond} then {self.then} else {self.else_})"
    
@dataclass
class Ifnz():
    cond: Expr
    then: Expr
    else_: Expr
    def __str__(self):
        return f"(if {self.cond} != 0 then {self.then} else {self.else_})"

@dataclass
class Letfun():
    name: str
    params: str
    bodyexpr: Expr
    inexpr: Expr
    def __str__(self) -> str:
        # params_with_commas = ", ".join(self.params)
        return f"letfun {self.name} ({self.params}) = {self.bodyexpr} in {self.inexpr} end"
    
@dataclass
class App():
    fun: Expr
    args: Expr
    def __str__(self) -> str:
        # args_with_comma = ", ".join(map(str, self.args))
        return f"({self.fun} ({self.args}))"

@dataclass
class Assign():
    name: str
    expr: Expr
    def __str__(self) -> str:
        return f"{self.name} := {self.expr}"

@dataclass
class Seq():
    expr1: Expr
    expr2: Expr
    def __str__(self) -> str:
        return f"({self.expr1}; {self.expr2})"

@dataclass
class Show():
    expr: Expr

@dataclass
class Read():
    def __str__(self) -> str:
        return "read"

# ----- Domain-specific extension (Tunes) ----- #

FILENAME = "answer.midi"
DEFAULT_TEMPO = 120 # 60 BPM = 1sec/BPM
DEFAULT_VOLUME = 100 # 0 - 127
DEFAULT_INSTRUMENT = 1 # 1 - 128
# Instruments defined here in better detail:
#   - "https://soundprogramming.net/file-formats/general-midi-instrument-list/"
# 1 - 8 (Piano)
# 9 - 16 (Chromatic percussion)
# 17 - 24 (Organ)
# 25 - 32 (Guitar)
# 33 - 40 (Bass)
# 41 - 48 (Strings)
# 49 - 56 (Strings Continued)
# 57 - 64 (Brass)
# 65 - 72 (Reed)
# 73 - 80 (Pipe)
# 81 - 88 (Synth Lead)
# 89 - 96 (Synth Pad)
# 97 - 104 (Synth Effects)
# 105 - 112 (Ethnic)
# 113 - 119 (Percussive)
# 120 - 128 (Sound Effects)


@dataclass
class Note():
    pitch: str # "C", "D", "E", "F", "G", "A", "B" or "R" for rest
    duration: Expr # in seconds (evaluated to an integer)
    volume: int = DEFAULT_VOLUME
    def __str__(self):
        return f"Note(Pitch: {self.pitch}, Duration: {self.duration}, Volume: {self.volume})"

@dataclass
class Tune():
    notes: list[Note]
    instrument: Expr
    def __str__(self):
        return f"Tune({', '.join(str(note) for note in self.notes)})(instrument: {self.instrument})"

@dataclass
class ConcatTunes():
    left: Tune
    right: Tune
    def __str__(self):
        return f"ConcatTunes({self.left}, {self.right})"

@dataclass
class Transpose():
    tune: Tune
    steps: Expr # in half-steps (evaluated to an integer)
    def __str__(self):
        return f"Transpose({self.tune}, {self.steps})"

@dataclass
class Repeat():
    tune: Tune | Note
    repetition: Expr
    def __str__(self):
        return f"Repeat({self.tune}, {self.repetition})"

@dataclass
class Volume():
    expr: Expr
    level: Expr
    def __str__(self):
        return f"Volume({self.expr}, {self.level})"

@dataclass
class Track():
    tracks: list[Note | Tune]
    def __str__(self):
        return f"Track({', '.join(str(track) for track in self.tracks)})"

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
    0:  "R",  # Rest
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

# model memory locations as (mutable) singleton lists
type Loc[V] = list[V] # always a singleton list
def newLoc[V](value: V) -> Loc[V]:
    return [value]
def getLoc[V](loc: Loc[V]) -> V:
    return loc[0]
def setLoc[V](loc: Loc[V], value: V) -> None:
    loc[0] = value

class EvalError(Exception):
    pass

type Value = int | bool | Note | Tune | Track | Closure

@dataclass
class Closure:
    param: str
    body: Expr
    env: Env[Value]

# ----- Tunes functions ----- #

def TransposeNote(tune: Tune, steps: int) -> Tune:
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

    return Tune(notes, tune.instrument)


def CreateMidiFile(tune: Tune | Track, instrument: int):    
    if isinstance(tune, Track):
        print("Creating MIDI file for Track")
        num_tracks = len(tune.tracks)
        midi = MIDIFile(numTracks=num_tracks)
        midi.addTempo(0, 0, DEFAULT_TEMPO)
        for idx, subexpr in enumerate(tune.tracks):
            notes = []
            match subexpr:
                case Note():
                    notes = [subexpr]
                case Tune():
                    notes = flatten_tune(subexpr)
                    instrument = subexpr.instrument
                case _:
                    raise EvalError("Track contains invalid expression")
            time = 0
            channel = idx
            midi.addProgramChange(idx, channel, time, instrument)

            for note in notes:
                duration = note.duration

                if note.pitch == "R":
                    time += duration
                    continue

                pitch = NOTE_TO_MIDI[note.pitch]
                midi.addNote(idx, channel, pitch, time, duration, note.volume)
                time += duration

        with open(FILENAME, "wb") as output_file:
            midi.writeFile(output_file)
        print(f"MIDI saves as {FILENAME}")

    elif isinstance(tune, Tune):
        # Original work for a single track
        print("Creating MIDI file for Tune")
        midi = MIDIFile(1)
        # # Set up MIDI structure 
        track = 0
        time = 0
        channel = instrument
        tempo = DEFAULT_TEMPO
        midi.addTempo(track, time, tempo)
        midi.addProgramChange(track, channel, time, tune.instrument)
        
        # Must flatten Tune first before writing notes
        flat_notes = flatten_tune(tune)

        for note in flat_notes:
            duration = note.duration

            if note.pitch == "R":
                time += duration
                continue

            pitch = NOTE_TO_MIDI[note.pitch]
            midi.addNote(track, channel, pitch, time, duration, note.volume)
            time += duration
        
        with open(FILENAME, "wb") as output_file:
            midi.writeFile(output_file)
        print(f"MIDI saves as {FILENAME}")
    elif isinstance(tune, Note):
        track = 0
        time = 0
        channel = instrument
        tempo = DEFAULT_TEMPO
        midi = MIDIFile(1)
        midi.addTempo(track, time, DEFAULT_TEMPO)
        midi.addProgramChange(track, channel, time, instrument)

        pitch = NOTE_TO_MIDI[tune.pitch]

        midi.addNote(track, channel, pitch, time, tune.duration, tune.volume)
        time += tune.duration

        with open(FILENAME, "wb") as output_file:
            midi.writeFile(output_file)
        print(f"MIDI saves as {FILENAME}")

def flatten_tune(tune: Tune) -> list[Note]:
    new_Tune = []
    for note in tune.notes:
        match note:
            case Note():
                new_Tune.append(note)
            case Tune():
                new_Tune.extend(flatten_tune(note))
            case _:
                raise EvalError("Tunes contains invalid type")
    return new_Tune

# ----- Evaluation ----- #

def eval(expr: Expr) -> Value:
    return evalInEnv(emptyEnv, expr)

def evalInEnv(env: Env[Loc[Value]], expr: Expr) -> Value:
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
            if right == 0:
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
            if not isinstance(left, bool):
                raise EvalError("And operator requires boolean operands")
            if left == False:
                return False
            right = evalInEnv(env, r)
            if not isinstance(right, bool):
                raise EvalError("And operator requires boolean operands")
            return right
        
        case Or(l, r):
            left = evalInEnv(env, l)
            if not isinstance(left, bool):
                raise EvalError("Or operator requires boolean operands")
            if left == True:
                return True
            right = evalInEnv(env, r)
            if not isinstance(right, bool):
                raise EvalError("Or operator requires boolean operands")
            return right

        case Not(e):
            value = evalInEnv(env, e)
            if not isinstance(value, bool):
                raise EvalError("Not operator requires boolean operands")
            return not value
        
        case Name(name):
            value = lookupEnv(name, env)
            if value is None:
                raise EvalError(f"unbound Name: {name}")
            return getLoc(value)
        
        case Let(name, defn, body):
            if name == "":
                raise EvalError("Name cannot be empty")
            if not isinstance(name, str):
                raise EvalError("Name must be a string")

            # Evaluate the definition and wrap it in a new location
            defn_val = evalInEnv(env, defn)
            loc = newLoc(defn_val)

            # Extend the environment with the name pointing to the location
            newEnv = extendEnv(name, loc, env)

            # evaluate the body in the extended environment
            return evalInEnv(newEnv, body)

            # # Get expression of name
            # new_defn = evalInEnv(env, defn)
            # # Extend env with name
            # newEnv = extendEnv(name, new_defn, env)
            # return evalInEnv(newEnv, body)
        
        case Eq(l, r): # Pretty sure i can just remove all if statements but the first one
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            # check if left and right are the same type
            # while also excepting mixed types, like int and bool
            if type(left) != type(right):
                return False  # Just return False if types don't match
            if isinstance(left, int) and isinstance(right, int):
                return left == right
            elif isinstance(left, bool) and isinstance(right, bool):
                return left == right
            elif isinstance(left, Tune) and isinstance(right, Tune):
                return left == right
            elif isinstance(left, Note) and isinstance(right, Note):
                return left == right
            else:
                raise EvalError("Must compare using int, bool, Tune, or Note types")
            
        case Neq(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            # check if left and right are the same type
            # while also excepting mixed types, like int and bool
            if type(left) != type(right):
                return False
            if isinstance(left, bool) and isinstance(right, bool):
                return left != right
            elif isinstance(left, int) and isinstance(right, int):
                return left != right
            elif isinstance(left, Tune) and isinstance(right, Tune):
                return left != right
            elif isinstance(left, Note) and isinstance(right, Note):
                return left != right
            else:
                raise EvalError("Must compare using int, bool, Tune, or Note types")
        
        case Lt(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if type(left) == int and type(right) == int:
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
            
        case If(c, t, e):
            cond = evalInEnv(env, c)
            if not isinstance(cond, bool):
                raise EvalError("If condition must be boolean")

            if cond: # if condition is true
                then_branch = evalInEnv(env, t)
                # if not isinstance(then_branch, (int, bool)):
                #     raise EvalError("If then must be int or bool")
                return then_branch
            else:   # condition is false
                else_branch = evalInEnv(env, e)
                # if not isinstance(else_branch, (int, bool)):
                #     raise EvalError("If else must be int or bool")
                return else_branch

        case Ifnz(c, t, e):
            cond = evalInEnv(env, c)
            if not isinstance(cond, int):
                raise EvalError("Ifnz condition must be an int")
            
            if cond: # if condition is true
                then_branch = evalInEnv(env, t)
                if not isinstance(then_branch, (int, bool)):
                    raise EvalError("Ifnz then must be int or bool")
                return then_branch
            else:   # condition is false
                else_branch = evalInEnv(env, e)
                if not isinstance(else_branch, (int, bool)):
                    raise EvalError("Ifnz else must be int or bool")
                return else_branch

        case Letfun(n, p, b, i):
            # Check for duplicate params
            # seen = [] # we will use this to check with "in" if the value is there twice
            # for param in p:
            #     if param in seen:
            #         raise EvalError("Duplicate parameter names in function definition: {p}")
            #     seen.append(i)
            c = Closure(p, b, env)
            l = newLoc(c)
            newEnv = extendEnv(n, l, env)
            c.env = newEnv
            return evalInEnv(newEnv, i)

        case App(f, a):
            fun = evalInEnv(env, f)
            if not isinstance(fun, Closure):
                raise EvalError("Attempted to call a non-function")
            # if len(fun.params) != len(a):
            #     raise EvalError(f"Function expects {len(fun.params)} arguments but got {len(a)}")
            arg = evalInEnv(env, a)
            # for arg in a:
            #     value = evalInEnv(env, arg)
            #     args.append(value)
            c: Closure = fun
            l = newLoc(arg)
            newEnv = extendEnv(c.param, l, c.env)
            # for i in range(len(fun.params)):
            #     name = fun.params[i]
            #     value = args[i]
            return evalInEnv(newEnv, c.body)

        case Assign(n, e1):
            l = lookupEnv(n, env)
            if l is None:
                raise EvalError(f"unbound name {n}")
            v_l = getLoc(l)
            if isinstance(v_l, Closure):
                raise EvalError(f"cannot assign to function name {n}")
            v = evalInEnv(env, e1)
            setLoc(l, v)
            return v
        
        case Seq(e1, e2):
            evalInEnv(env, e1)
            return evalInEnv(env, e2)

        case Show(e):
            # evaluate e to a value v
            v = evalInEnv(env, e)
            # Show v in a suitable way
            match v:
                case int() | bool():
                    print(v)
                case Note() | Tune() | Track():
                    print("showing midi file")
                    CreateMidiFile(v, 0)
                    os.startfile(FILENAME)
            return v
        
        case Read():
            user_input = input("Enter an integer >> ")
            # try if the input is int, else throw exception
            try:
                return int(user_input)
            except ValueError:
                raise EvalError(f"Expected an integer, got: {user_input}")
                

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
        
        case Tune(n, ins):
            if not isinstance(n, list):
                raise EvalError("Tunes must be a list of notes")
            instrument = evalInEnv(env, ins)
            if not isinstance(instrument, int):
                raise EvalError("Tune must be an integer expression for instruments")
            if instrument < 1 or instrument > 128:
                raise EvalError("instrument must be between 1 - 128")
            # Check if all elements in the list (n) are valid objects
            result = []
            for note in n:
                if not isinstance(note, (Tune, Note, Repeat, Volume)):
                    raise EvalError("Tunes must contain only Tune or Note objects")
                note_value = evalInEnv(env, note)
                result.append(note_value)
            return Tune(result, instrument-1)

        case ConcatTunes(l, r):
            left = evalInEnv(env, l)
            right = evalInEnv(env, r)
            if not isinstance(left, Tune) or not isinstance(right, Tune):
                raise EvalError("ConcatTunes must be two Tunes")
            return Tune(left.notes + right.notes, left.instrument + right.instrument)

        case Transpose(t, s):
            if not isinstance(t, Tune):
                raise EvalError("Transpose can only tune up or down Tunes")
            steps = evalInEnv(env, s)
            if not isinstance(steps, int):
                raise EvalError("Transpose steps must be an integer")
            return TransposeNote(evalInEnv(env, t), steps)

        case Repeat(t, r):
            # evaluate Tunes (t) and Expr (r) before repeating
            t_v = evalInEnv(env, t)
            r_v = evalInEnv(env, r)
            # check if either values are of correct types
            # if not isinstance(t_v, (Tune, Note, Volume, Repeat)): # yes i am allowing Repeat over Repeat, i am aware
            #     raise EvalError("Repeat expects a Tune, Note, Volume, or Repeat object")
            if not isinstance(r_v, int):
                raise EvalError("Repeat expects an int for repetition")
            if isinstance(t_v, Repeat):
                t_v = evalInEnv(env, t_v)
            # return the Tune or Note that is to be repeated on r times
            match t_v:
                case Tune(n, ins):
                    return Tune(n * r_v, ins)
                case Note(name, d):
                    return Tune([Note(name, d)] * r_v, instrument=DEFAULT_INSTRUMENT)
                case _:
                    raise EvalError("Repeat contains invalid expression")

        case Volume(t, l):
            # evaluate Note (t) and Expr (l) before changing volume
            t_v = evalInEnv(env, t)
            l_v = evalInEnv(env, l)
            if not isinstance(t_v, Note):
                raise EvalError("Volume expects a Note")
            if not isinstance(l_v, int):
                raise EvalError("Volume expects an integer for its volume level")
            if not (0 <= l_v <= 127):
                raise EvalError("volume level must be between 0 and 127")
            return Note(t_v.pitch, t_v.duration, volume=l_v) # return a note for modified volume

        case Track(t):
            t_v = [evalInEnv(env, e) for e in t]
            if len(t_v) < 1 or len(t_v) > 16:
                raise EvalError("Track can only contain 0 - 16 individual tracks")
            if not all(isinstance(ev, Tune) for ev in t_v):
                raise EvalError("Track expects only Tune objects")
            return Track(t_v)

        case _:
            raise EvalError(f"unknown expression: {expr}")


def run(expr: Expr) -> None:
    print(f"Running: {expr}")
    try:
        result = eval(expr)
        match result: 
            case int() | bool():
                print(f"Result: {result}\n")
            
            case Tune() | Track():
                if type(expr) == ConcatTunes or type(expr) == Transpose:
                    print(f"Result: {result}")

                CreateMidiFile(result, 1)
                print() # Creates new line
                # os.startfile(FILENAME) # This is for Windows only

            case Note():
                print(f"Result: {result}\n")

    except EvalError as err:
        print("ERROR: ", err, "\n")


# math : Expr = Add(Lit(1), Mul(Lit(2), Lit(3)))
# run(math)

# letbinding : Expr = Let("x", Lit(1), Add(Name("x"), Lit(2)))
# run(letbinding)

# ifnz : Expr = Ifnz(Add(Lit(3), Neg(Lit(1))), Lit(True), Lit(False))
# run(ifnz)

# # ----- Demonstration of DSL and its Features ----- #
# a : Expr = Note("C", Lit(1))
# run (a)
# # Result: Note(Pitch: C, Duration: 1)

# b : Expr = Note("C", Add(Lit(1), Lit(2)))
# run (b)
# # Result: Note(Pitch: C, Duration: 3)

# c : Expr = Tune([a, b], Lit(1))
# run (c)
# # MIDI saves as answer.midi

# d : Expr = Tune([Note("A", Lit(1)), Note("B", Lit(2))], Lit(1))
# run (d)
# # MIDI saves as answer.midi

# e: Expr = ConcatTunes(c, d)
# run (e)
# # Result: Tune[Note(Pitch: C, Duration: 1), Note(Pitch: C, Duration: 3), Note(Pitch: A, Duration: 1), Note(Pitch: B, Duration: 2)]
# # MIDI saves as answer.midi

# f: Expr = Transpose(d, Lit(1))
# run (f)
# # Result: Tune[Note(Pitch: A#, Duration: 1), Note(Pitch: C, Duration: 2)]
# # MIDI saves as answer.midi

# # Simple song test
# twinkle_star : Expr = Tune([
#     Note("C", Lit(1)), Note("C", Lit(1)), Note("G", Lit(1)), Note("G", Lit(1)),
#     Note("A", Lit(1)), Note("A", Lit(1)), Note("G", Lit(2)),

#     Note("F", Lit(1)), Note("F", Lit(1)), Note("E", Lit(1)), Note("E", Lit(1)),
#     Note("D", Lit(1)), Note("D", Lit(1)), Note("C", Lit(2)),
# ], Lit(10))
# run(twinkle_star)
# # MIDI saves as answer.midi


