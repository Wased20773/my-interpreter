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
        return Note(pitch_token.value, duration_expr)
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

# For quick testing, uncomment below code
driver()

# ----- Demonstration of DSL's concrete syntax ----- #
# just_parse("note C for 3 seconds")
# # raw AST:  Note(pitch='C', duration=Lit(value=3))

# just_parse("tune { note C for 1 seconds, note B for 2 seconds, note A for 3 seconds }")
# # raw AST:  Tune(notes=[Note(pitch='C', duration=Lit(value=1)), Note(pitch='B', duration=Lit(value=2)), Note(pitch='A', duration=Lit(value=3))])

# just_parse("tune { note C for 1 seconds, note B for 2 seconds } ++ tune { note A for 3 seconds }")
# # raw AST:  ConcatTunes(left=Tune(notes=[Note(pitch='C', duration=Lit(value=1)), Note(pitch='B', duration=Lit(value=2))]), right=Tune(notes=[Note(pitch='A', duration=Lit(value=3))]))

# just_parse("transpose tune { note C for 1 seconds, note B for 2 seconds, note A for 3 seconds} by 3")
# # raw AST:  Transpose(tune=Tune(notes=[Note(pitch='C', duration=Lit(value=1)), Note(pitch='B', duration=Lit(value=2)), Note(pitch='A', duration=Lit(value=3))]), steps=Lit(value=3))

# just_parse("transpose tune { note A for 1 seconds, note B for 2 seconds } by -1")
# # raw AST:  Transpose(tune=Tune(notes=[Note(pitch='A', duration=Lit(value=1)), Note(pitch='B', duration=Lit(value=2))]), steps=Neg(expr=Lit(value=1)))

# just_parse("tune {}")
# # raw AST:  Tune(notes=[])

# just_parse("tune { note E for 1 seconds } ++ tune { note F for 2 seconds }")
# raw AST:  ConcatTunes(left=Tune(notes=[Note(pitch='E', duration=Lit(value=1))]), right=Tune(notes=[Note(pitch='F', duration=Lit(value=2))]))