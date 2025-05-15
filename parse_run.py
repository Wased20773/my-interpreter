from interp import Lit, Add, Sub, Mul, Div, Neg, And, Or, Not, Let, Name, Eq, Lt, If, Letfun, App, \
Ifnz, Expr, run

from lark import Lark, Token, ParseTree, Transformer
from lark.exceptions import VisitError
from pathlib import Path

parser = Lark(Path('expr.lark').read_text(), start='expr', parser='earley', ambiguity='explicit')

class ParseError(Exception):
    pass

def parse(s: str) -> ParseTree:
    try:
        return parser.parse(s)
    except Exception as e:
        raise ParseError(e)
    
class AmbiguousParse(Exception):
    pass

class ToExpr(Transformer[Token, Expr]):
    def plus(self, args:tuple[Expr,Expr]) -> Expr:
        return Add(args[0],args[1])
    def minus(self, args:tuple[Expr,Expr]) -> Expr:
        return Sub(args[0],args[1])
    def times(self, args:tuple[Expr,Expr]) -> Expr:
        return Mul(args[0],args[1])
    def divide(self, args:tuple[Expr,Expr]) -> Expr:
        return Div(args[0],args[1])
    def neg(self, args:tuple[Expr]) -> Expr:
        return Neg(args[0])
    # Missing definitions (REQUIRED)
    #   - And
    #   - Or
    #   - Not
    def let(self, args:tuple[Token,Expr,Expr]) -> Expr:
        return Let(args[0].value,args[1],args[2])
    # Missing definitions (REQUIRED)
    #   - Eq
    #   - Lt
    #   - If
    # Missing definitions (NOT REQUIRED)
    #   - LorE
    #   - Gt
    #   - GorE
    def id(self, args:tuple[Token]) -> Expr:
        return Name(args[0].value)
    def int(self,args:tuple[Token]) -> Expr:
        return Lit(int(args[0].value))
    def ifnz(self,args:tuple[Expr,Expr,Expr]) -> Expr: # Not in test
        return Ifnz(args[0],args[1],args[2])
    def param_list(self,args:tuple[Token]) -> list[str]:
        if args and args[0] is None:
            return []
        return [token.value for token in args]
    def arg_list(self,args:tuple[Expr]) -> list[Expr]:
        if args and args[0] is None:
            return []
        return list(args)
    def letfun(self,args:tuple[Token,list[str],Expr,Expr]) -> Expr:
        return Letfun(args[0].value,args[1],args[2],args[3])
    def app(self,args:tuple[Expr,list[Expr]]) -> Expr:
        return App(args[0],args[1])    
    # Missing definitions (REQUIRED)
    #   - DSL (Note, Tune, ConcatTunes, Transpose) ... Probably?
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

driver()