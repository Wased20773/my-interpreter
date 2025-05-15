from interp import Lit, Add, Sub, Mul, Div, Neg, And, Or, Not, Let, Name, Eq, Lt, If, Letfun, App, \
Ifnz, Neq, LorE, Gt, GorE, Expr, Note, Tune, ConcatTunes, Transpose, run

from lark import Lark, Token, ParseTree, Transformer
from lark.exceptions import VisitError
from pathlib import Path

parser = Lark(Path('expr.lark').read_text(), start='expr1', parser='earley', ambiguity='explicit')

class ParseError(Exception):
    pass

# uncomment code for detailed tree
def parse_and_run(s: str) -> ParseTree:
    try:
        t = parser.parse(s)
        # print("raw: ", t)
        # print("pretty:")
        # print(t.pretty())
        ast = genAST(t)
        # print("raw AST: ", repr(ast))
        return run(ast)
    except AmbiguousParse:
        print("ambiguous parse")
    except ParseError as e:
        print("parse error:")
        print(e)
    except Exception as e:
        raise ParseError(e)

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
    def ifnz(self,args: tuple[Expr, Expr, Expr]) -> Expr: # Not in test
        return Ifnz(args[0], args[1], args[2])
    def param_list(self, args: tuple[Token]) -> list[str]:
        if args and args[0] is None:
            return []
        return [token.value for token in args]
    def arg_list(self, args: tuple[Expr]) -> list[Expr]:
        if args and args[0] is None:
            return []
        return list(args)
    def note_list(self, args: tuple[Expr]) -> list[Expr]:
        if args and args[0] is None:
            return []
        return list(args)
    def letfun(self, args: tuple[Token, list[str], Expr, Expr]) -> Expr:
        return Letfun(args[0].value, args[1], args[2], args[3])
    def app(self, args: tuple[Token, list[Expr]]) -> Expr:
        return App(Name(args[0].value), args[1])    
    def note(self, args: tuple[Token, Token]) -> Expr:
        pitch_token, duration_token = args
        return Note(pitch_token.value, Lit(int(duration_token.value)))
    def tune(self, args: list[Expr]) -> Expr:
        return Tune(args[0])
    def concat_tunes(self, args: tuple[Expr, Expr]) -> Expr:
        return ConcatTunes(args[0], args[1])
    def transpose(self, args: tuple[Expr, Expr]) -> Expr:
        return Transpose(args[0], args[1])
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

# For quick testing, uncomment below code
# driver()

# ----- Demonstration of DSL's concrete syntax ----- #
parse_and_run("note C for 3 seconds")
# Result: Note(Pitch: C, Duration: 3)

parse_and_run("tune { note C for 1 seconds, note B for 2 seconds, note A for 3 seconds }")
# MIDI saves as answer.midi

parse_and_run("tune { note C for 1 seconds, note B for 2 seconds } ++ tune { note A for 3 seconds }")
# Result: Tune[Note(Pitch: C, Duration: 1), Note(Pitch: B, Duration: 2), Note(Pitch: A, Duration: 3)]
# MIDI saves as answer.midi

parse_and_run("transpose tune { note C for 1 seconds, note B for 2 seconds, note A for 3 seconds} by 3")
# Result: Tune[Note(Pitch: D#, Duration: 1), Note(Pitch: D, Duration: 2), Note(Pitch: C, Duration: 3)]
# MIDI saves as answer.midi

parse_and_run("transpose tune { note A for 1 seconds, note B for 2 seconds } by -1")
# Result: Tune[Note(Pitch: G#, Duration: 1), Note(Pitch: A#, Duration: 2)]
# MIDI saves as answer.midi

parse_and_run("tune {}")
# MIDI saves as answer.midi

parse_and_run("tune { note E for 1 seconds } ++ tune { note F for 2 seconds }")
# Result: Tune[Note(Pitch: E, Duration: 1), Note(Pitch: F, Duration: 2)]
# MIDI saves as answer.midi