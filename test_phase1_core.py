import unittest

from interp import Lit, Add, Sub, Mul, Div, Neg, And, Or, Not, Let, Name, Let, EvalError

class TestExpr(unittest.TestCase):
    def eval(self, expr, expected):
        from interp import eval
        self.assertEqual(eval(expr), expected)

    def test_Add(self):
        self.eval(Add(Add(Lit(5), Lit(2)), Lit(8)), 15)
        self.eval(Add(Add(Lit(3.8), Lit(0.2)), Lit(1)), 5.0)

        from interp import eval

        with self.assertRaises(EvalError) as context:
            eval(Add(Lit(5), Lit(True)))
        self.assertEqual(str(context.exception), "cannot add boolean values")

        with self.assertRaises(EvalError) as context:
            eval(Add(Lit("hello"), Lit(2)))
        self.assertEqual(str(context.exception), "addition operator requires numeric operands")

    def test_Sub(self):
        self.eval(Sub(Lit(5), Lit(1)), 4)
        self.eval(Sub(Lit(5.5), Lit(2.5)), 3.0)
        self.eval(Sub(Lit(5), Lit(5)), 0)

        from interp import eval

        with self.assertRaises(EvalError) as context:
            eval(Sub(Lit(5), Lit(True)))
        self.assertEqual(str(context.exception), "cannot subtract boolean values")
        
        with self.assertRaises(EvalError) as context:
            eval(Sub(Lit("hello"), Lit(2)))
        self.assertEqual(str(context.exception), "subtraction operator requires numeric operands")

    def test_Mul(self):
        self.eval(Mul(Add(Add(Lit(4), Lit(2)), Neg(Lit(2))), Lit(2)), 8)
        self.eval(Mul(Lit(3.8), Lit(0.2)), 0.76)
        self.eval(Mul(Lit(5), Neg(Lit(1))), -5)

        from interp import eval

        with self.assertRaises(EvalError) as context:
            eval(Mul(Lit(5), Lit(True)))
        self.assertEqual(str(context.exception), "cannot multiply boolean values")
        
        with self.assertRaises(EvalError) as context:
            eval(Mul(Lit("hello"), Lit(2)))
        self.assertEqual(str(context.exception), "multiplication operator requires numeric operands")

    def test_Div(self):
        self.eval(Div(Add(Lit(4), Lit(2)), Lit(2)), 3)
        self.eval(Div(Lit(5), Lit(2)), 2.5)
        self.eval(Div(Lit(0), Lit(4)), 0)
        
        from interp import eval
        
        with self.assertRaises(EvalError) as context:
            eval(Div(Lit(5), Lit(True)))
        self.assertEqual(str(context.exception), "cannot divide boolean values")
        
        with self.assertRaises(EvalError) as context:
            eval(Div(Lit("hello"), Lit(2)))
        self.assertEqual(str(context.exception), "division operator requires numeric operands")
        
        with self.assertRaises(EvalError) as context:
            eval(Div(Lit(4), Lit(0)))
        self.assertEqual(str(context.exception), "division by zero")
        

    def test_Neg(self):
        self.eval(Neg(Add(Lit(5), Lit(2))), -7)
        self.eval(Neg(Lit(-5)), 5)
        self.eval(Neg(Lit(5)), -5)
        self.eval(Neg(Lit(0)), 0)

        from interp import eval

        with self.assertRaises(EvalError) as context:
            eval(Neg(Lit(True)))
        self.assertEqual(str(context.exception), "cannot negate boolean values")
        
        with self.assertRaises(EvalError) as context:
            eval(Neg(Lit("hello")))
        self.assertEqual(str(context.exception), "negation operator requires numeric operands")

    def test_And(self):
        self.eval(And(Lit(True), Lit(True)), True)
        self.eval(And(Lit(True), Lit(False)), False)
        self.eval(And(Lit(False), Lit(True)), False)
        self.eval(And(Lit(False), Lit(False)), False)

        from interp import eval

        with self.assertRaises(EvalError) as context:
            eval(And(Lit(True), Lit(5)))
        self.assertEqual(str(context.exception), "and operator requires boolean operands")

    def test_Or(self):
        self.eval(Or(Lit(True), Lit(True)), True)
        self.eval(Or(Lit(True), Lit(False)), True)
        self.eval(Or(Lit(False), Lit(True)), True)
        self.eval(Or(Lit(False), Lit(False)), False)

        from interp import eval
        with self.assertRaises(EvalError) as context:
            eval(Or(Lit(True), Lit(5)))
        self.assertEqual(str(context.exception), "or operator requires boolean operands")

    def test_Not(self):
        self.eval(Not(Lit(True)), False)
        self.eval(Not(Lit(False)), True)

        from interp import eval

        with self.assertRaises(EvalError) as context:
            eval(Not(Lit(5)))
        self.assertEqual(str(context.exception), "not operator requires boolean operands")

    def test_Name(self):
        from interp import eval

        with self.assertRaises(EvalError) as context:
            eval(Name("x"))
        self.assertEqual(str(context.exception), "unbound name: x")

    def test_Let(self):
        self.eval(Let("x", Add(Lit(1), Lit(2)), Sub(Name("x"), Lit(3))), 0)
        self.eval(Let("x", Lit(5), (Let("y", Lit(2), Add(Name("x"), Name("y"))))), 7)
        self.eval(Let("x", Lit(5), (Let("y", Lit(2), (Let("x", Lit(2), Add(Name("x"), Name("y"))))))), 4)
        self.eval(Let("x", Lit(5), Add(Name("x"), Lit(2))), 7)

        from interp import eval
        
        with self.assertRaises(EvalError) as context:
            eval(Let("", Lit(5), Add(Name("x"), Lit(2))))
        self.assertEqual(str(context.exception), "name cannot be empty")