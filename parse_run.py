from interp import Lit, Add, Sub, Mul, Div, Neg, And, Or, Not, Let, Name, Eq, Lt, If, Letfun, App, Assign, Seq, Show, Read, \
Ifnz, Neq, LorE, Gt, GorE, Expr, Note, Tune, ConcatTunes, Transpose, Repeat, Volume, Track, run

from lark import Lark, Token, ParseTree, Transformer
from lark.exceptions import VisitError
from pathlib import Path

parser = Lark(Path('expr.lark').read_text(), start='expr0', parser='earley', ambiguity='explicit')

class ParseError(Exception):
    pass

# uncomment code for detailed tree
def just_parse(s:str) -> (Expr|None):   
    '''Parses and pretty-prints an expression'''
    try:
        t = parse(s)
        print("raw:", t)
        print("pretty:")
        print(t.pretty())
        ast = genAST(t)
        print("raw AST:", repr(ast))  # use repr() to avoid str() pretty-printing
        return ast
    except AmbiguousParse:
        print("ambiguous parse")
    except ParseError as e:
        print("parse error:")
        print(e)

# Used in kahoots with driver()
def parse(s:str) -> ParseTree:
    try:
        return parser.parse(s)
    except Exception as e:
        raise ParseError(e)


class AmbiguousParse(Exception):
    pass

class ToExpr(Transformer[Token, Expr]):
    def plus(self, args: tuple[Expr, Expr]) -> Expr:
        return Add(args[0], args[1])
    def minus(self, args: tuple[Expr, Expr]) -> Expr:
        return Sub(args[0], args[1])
    def times(self, args: tuple[Expr, Expr]) -> Expr:
        return Mul(args[0], args[1])
    def divide(self, args: tuple[Expr, Expr]) -> Expr:
        return Div(args[0], args[1])
    def neg(self, args: tuple[Expr]) -> Expr:
        return Neg(args[0])
    def or_expr(self, args: tuple[Expr, Expr]) -> Expr:
        return Or(args[0], args[1])
    def and_expr(self, args: tuple[Expr, Expr]) -> Expr:
        return And(args[0], args[1])
    def not_expr(self, args: tuple[Expr]) -> Expr:
        return Not(args[0])
    def let(self, args: tuple[Token, Expr, Expr]) -> Expr:
        return Let(args[0].value, args[1], args[2])
    def neq(self, args: tuple[Expr, Expr, Expr]) -> Expr:
        return Neq(args[0], args[1])
    def eq(self, args: tuple[Expr, Expr]) -> Expr:
        return Eq(args[0], args[1])
    def lt(self, args: tuple[Expr, Expr]) -> Expr:
        return Lt(args[0], args[1])
    def if_expr(self, args: tuple[Expr, Expr, Expr]) -> Expr:
        return If(args[0], args[1], args[2])
    def lore(self, args: tuple[Expr, Expr]) -> Expr:
        return LorE(args[0], args[1])
    def gt(self, args: tuple[Expr, Expr]) -> Expr:
        return Gt(args[0], args[1])
    def gore(self, args: tuple[Expr, Expr]) -> Expr:
        return GorE(args[0], args[1])
    def id(self, args: tuple[Token]) -> Expr:
        return Name(args[0].value)
    def int(self,args: tuple[Token]) -> Expr:
        return Lit(int(args[0].value))
    def true(self, args: tuple[Token]) -> Expr:
        return Lit(True)
    def false(self, args: tuple[Token]) -> Expr:
        return Lit(False)
    def ifnz(self,args: tuple[Expr, Expr, Expr]) -> Expr:
        return Ifnz(args[0], args[1], args[2])
    # def param_list(self, args: tuple[Token]) -> str:
    #     if args and args[0] is None:
    #         return []
    #     return args[0].value
    # def arg_list(self, args: tuple[Expr]) -> Expr:
    #     # if args and args[0] is None:
    #     #     return []
    #     return args[0]
    def note_list(self, args: tuple[Expr]) -> list[Expr]:
        if args and args[0] is None:
            return []
        return list(args)
    def letfun(self, args: tuple[Token, Name, Expr, Expr]) -> Expr:
        return Letfun(args[0].value, args[1].varname, args[2], args[3])
    def app(self, args: tuple[Expr, Expr]) -> Expr:
        if isinstance(args[0], Name):
            return App(Name(args[0].varname), args[1])
        elif isinstance(args[0], App):
            return App(args[0], args[1])
        else:
            return App(args[0], args[1])
    def assign(self, args: tuple[Token, Expr]) -> Expr:
        return Assign(args[0].value, args[1])
    def seq(self, args: tuple[Expr, Expr]) -> Expr:
        return Seq(args[0], args[1])
    def show(self, args: tuple[Expr]) -> Expr:
        return Show(args[0])
    def read(self, args) -> Expr:
        return Read()
    # --- DSL --- #
    def note(self, args: tuple[Token, Expr]) -> Expr:
        pitch_token, duration_expr = args
        return Note(str(pitch_token), duration_expr)
    def tune(self, args: list[Expr, Expr]) -> Expr:
        return Tune(args[0], args[1])
    def concat_tunes(self, args: tuple[Expr, Expr]) -> Expr:
        return ConcatTunes(args[0], args[1])
    def transpose(self, args: tuple[Expr, Expr]) -> Expr:
        return Transpose(args[0], args[1])
    def repeat(self, args: tuple[Expr, Expr]) -> Expr:
        return Repeat(args[0], args[1])
    def volume(self, args: tuple[Expr, Expr]) -> Expr:
        return Volume(args[0], args[1])
    def track(self, args: list[Expr]) -> Expr:
        return Track(args[0])
    def _ambig(self,_) -> Expr:    # ambiguity marker
        raise AmbiguousParse()

def genAST(t: ParseTree) -> Expr:
    try:
        return ToExpr().transform(t)
    except VisitError as e:
        if isinstance(e.orig_exc, AmbiguousParse):
            raise AmbiguousParse()
        else:
            raise e
        
def driver():
    while True:
        try:
            s = input('expr: ')
            t = parse(s)
            print("raw: ", t)
            print("pretty:")
            print(t.pretty())
            ast = genAST(t)
            print("raw AST:", repr(ast))
            run(ast)
        except AmbiguousParse:
            print("ambiguous parse")
        except ParseError as e:
            print("parse error:")
            print(e)
        except EOFError:
            break

def myDriver(s:str):
    t = parse(s)
    print("raw: ", t)
    print("pretty: ")
    print(t.pretty())
    ast = genAST(t)
    print("raw AST:", repr(ast))
    run(ast)

# For quick testing, uncomment below code
# driver()

# ----- Demonstration of DSL's concrete syntax ----- #
'''
Things to consider when creating concrete examples of my DSL
    - Check interp.py for the list of instrument values (lines 283 - 300)
    - Check interp.py for MIDI values of notes (lines 352 - 371)
    - Volume is in the range 0 (silent) to 127 (maximum)
    - Instruments range from 0-127 (General MIDI Instrument)
    - Repeat works best with Tunes and Notes, might act weird with 
      other operators
    - Track will allow for multiple tunes to play with their individual
      instrument.
'''
# -------------------------------------------------- #
# 1. Basic melody with a single instrument
# basic = '''
# show tune [ note C for 1 seconds, note D for 1 seconds, note E for 1 seconds ] (1)
# '''
# myDriver(basic)

# -------------------------------------------------- #
# 2. Melody with dynamic volume (volume read from user)
# volume_input = '''
# show tune [ volume (note A for 3 seconds, read) ] (5)
# '''
# myDriver(volume_input)

# -------------------------------------------------- #
# 3. Repeat a melody pattern by multiple times
# repeat = '''
# show repeat ( tune [ note C for 1 seconds, note D for 1 seconds, note E for 1 seconds ] (1) , 3)
# '''
# myDriver(repeat)

# -------------------------------------------------- #
# 4. Multi-instrument track demo for a simple beat (instrument
# read from user)
# Suggested values to ues: 116 and 116
# beat = '''
# show track [ repeat ( tune [ note G4 for 1 seconds, note B4 for 1 seconds] (read), 10), repeat (tune [ note R for 1 seconds, note C4 for 1 seconds, note R for 1 seconds, note F4 for 1 seconds ] (read), 5)]
# '''
# myDriver(beat)
# -------------------------------------------------- #
# ---------- Below are favorites for certain instruments -------------- #
FX1 = 97    # good vibrating beat
FX6 = 102   # good ambiance noise
Drawbar_Organ = 17 # constant deep sound
Electric_Base = 34 # good guitar bass
current = 37
# ---------- Below are my custom songs -------------- #
# 1. Basic beat
drums = f'''
show track [ repeat ( tune [ note C1 for 1 seconds, note R for 1 seconds, note C1 for 1 seconds, note R for 1 seconds, note C1 for 1 seconds, note R for 1 seconds, note C1 for 1 seconds, note R for 1 seconds, note C#1 for 1 seconds, note D1 for 1 seconds, note D#1 for 1 seconds, note E1 for 1 seconds, note F1 for 1 seconds, note F#1 for 1 seconds, note G1 for 1 seconds, note G#1 for 1 seconds, note A1 for 1 seconds, note A#1 for 1 seconds, note B1 for 1 seconds]({current}), 5) ]
'''


# --------- Below are all octaves from -1 to 9 --------- #
octave_negativeOne = f'''
show track [ repeat (tune [ note C-1 for 1 seconds, note D-1 for 1 seconds, note E-1 for 1 seconds, note F-1 for 1 seconds, note G-1 for 1 seconds, note A-1 for 1 seconds, note B-1 for 1 seconds]({current}), 20) ]
'''
octave_zero = f'''
show track [ repeat (tune [ note C0 for 1 seconds, note D0 for 1 seconds, note E0 for 1 seconds, note F0 for 1 seconds, note G0 for 1 seconds, note A0 for 1 seconds, note B0 for 1 seconds]({current}), 20) ]
'''
octave_one = f'''
show track [ repeat (tune [ note C1 for 1 seconds, note D1 for 1 seconds, note E1 for 1 seconds, note F1 for 1 seconds, note G1 for 1 seconds, note A1 for 1 seconds, note B1 for 1 seconds]({current}), 20) ]
'''
octave_two = f'''
show track [ repeat (tune [ note C2 for 1 seconds, note D2 for 1 seconds, note E2 for 1 seconds, note F2 for 1 seconds, note G2 for 1 seconds, note A2 for 1 seconds, note B2 for 1 seconds]({current}), 20) ]
'''
octave_three = f'''
show track [ repeat (tune [ note C3 for 1 seconds, note D3 for 1 seconds, note E3 for 1 seconds, note F3 for 1 seconds, note G3 for 1 seconds, note A3 for 1 seconds, note B3 for 1 seconds]({current}), 20) ]
'''
octave_four = f'''
show track [ repeat (tune [ note C4 for 1 seconds, note D4 for 1 seconds, note E4 for 1 seconds, note F4 for 1 seconds, note G4 for 1 seconds, note A4 for 1 seconds, note B4 for 1 seconds]({current}), 20) ]
'''
octave_five = f'''
show track [ repeat (tune [ note C5 for 1 seconds, note D5 for 1 seconds, note E5 for 1 seconds, note F5 for 1 seconds, note G5 for 1 seconds, note A5 for 1 seconds, note B5 for 1 seconds]({current}), 20) ]
'''
octave_six = f'''
show track [ repeat (tune [ note C6 for 1 seconds, note D6 for 1 seconds, note E6 for 1 seconds, note F6 for 1 seconds, note G6 for 1 seconds, note A6 for 1 seconds, note B6 for 1 seconds]({current}), 20) ]
'''
octave_seven = f'''
show track [ repeat (tune [ note C7 for 1 seconds, note D7 for 1 seconds, note E7 for 1 seconds, note F7 for 1 seconds, note G7 for 1 seconds, note A7 for 1 seconds, note B7 for 1 seconds]({current}), 20) ]
'''
octave_eight = f'''
show track [ repeat (tune [ note C8 for 1 seconds, note D8 for 1 seconds, note E8 for 1 seconds, note F8 for 1 seconds, note G8 for 1 seconds, note A8 for 1 seconds, note B8 for 1 seconds]({current}), 20) ]
'''
octave_nine = f'''
show track [ repeat (tune [ note C9 for 1 seconds, note D9 for 1 seconds, note E9 for 1 seconds, note F9 for 1 seconds, note G9 for 1 seconds, note A9 for 1 seconds, note B9 for 1 seconds]({current}), 20) ]
'''

# target temp is 480
# intro beat is 48 seconds loop (0 - length)
# middle starts after 48*4, slightly faster with more notes playing (25sec - length)
# end beat is 48 seconds loop (somewhere - length)

cooking = f'''
show track 
    [ 
        repeat (
            tune [
                volume(note D1 for 1 seconds, 127),
                volume(note R for 2 seconds, 127),
                volume(note D1 for 1 seconds, 127),
                volume(note R for 2 seconds, 127),
                volume(note F1 for 1 seconds, 127),
                volume(note R for 5 seconds, 127)
            ]({Drawbar_Organ}), 76
        ),
        
        tune [
            repeat (
                tune [
                    volume (note C4 for 48 seconds, 100),
                    volume (note C3 for 48 seconds, 100)
                ]({FX1}), 8
            )
        ]({FX1}),

        tune [
            note R for 192 seconds,
            repeat (
                tune [
                    volume(note A6 for 1 seconds, 60),
                    volume(note R for 47 seconds, 60),
                    volume(note F#7 for 1 seconds, 60),
                    volume(note G7 for 1 seconds, 60),
                    volume(note G#7 for 1 seconds, 60),
                    volume(note A7 for 1 seconds, 60),
                    volume(note R for 44 seconds, 60)
                ](10), 8
            )
        ](10),

        tune [
            note R for 192 seconds,
            repeat(
                tune [
                    volume(note A3 for 24 seconds, 100),
                    volume(note B3 for 12 seconds, 100),
                    volume(note A#3 for 12 seconds, 100),
                    volume(note A3 for 24 seconds, 100),
                    volume(note F3 for 12 seconds, 100),
                    volume(note E3 for 12 seconds, 100)
                ](18), 9
            ),
            tune [
                volume(note A3 for 18 seconds, 100)
            ](18)
        ] (18)
    ]
'''
# 

# -------------- Test strings below ----------------- #
myDriver(cooking)