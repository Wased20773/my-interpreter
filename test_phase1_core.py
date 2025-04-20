import unittest

from interp import Lit, Add, Sub, Mul, Div, Neg, And, Or, Not, Let, Name, Let, EvalError

class TestExpr(unittest.TestCase):
    def eval(self, expr, expected):
        from interp import eval
        self.assertEqual(eval(expr), expected)

    def test_Add(self):
        # Test addition of two literals
        self.eval(Add(Add(Lit(5), Lit(2)), Lit(8)), 15)

        from interp import eval

        # Testing with float literals
        with self.assertRaises(EvalError) as context:
            eval(Add(Add(Lit(3.8), Lit(0.2)), Lit(1)))
        self.assertEqual(str(context.exception), "addition operator requires integer operands")

        # Testing with boolean literals
        with self.assertRaises(EvalError) as context:
            eval(Add(Lit(5), Lit(True)))
        self.assertEqual(str(context.exception), "cannot add boolean values")

        # Testing with string literals
        with self.assertRaises(EvalError) as context:
            eval(Add(Lit("hello"), Lit(2)))
        self.assertEqual(str(context.exception), "addition operator requires integer operands")

    def test_Sub(self):
        # Test subtraction of two literals
        self.eval(Sub(Lit(5), Lit(1)), 4)
        self.eval(Sub(Lit(5), Lit(5)), 0)

        from interp import eval

        # Testing with float literals
        with self.assertRaises(EvalError) as context:
            eval(Sub(Lit(5.5), Lit(2.5)))
        self.assertEqual(str(context.exception), "subtraction operator requires integer operands")
        
        # Testing with boolean literals
        with self.assertRaises(EvalError) as context:
            eval(Sub(Lit(5), Lit(True)))
        self.assertEqual(str(context.exception), "cannot subtract boolean values")
        
        # Testing with string literals
        with self.assertRaises(EvalError) as context:
            eval(Sub(Lit("hello"), Lit(2)))
        self.assertEqual(str(context.exception), "subtraction operator requires integer operands")

    def test_Mul(self):
        # Test multiplication of two literals
        self.eval(Mul(Add(Add(Lit(4), Lit(2)), Neg(Lit(2))), Lit(2)), 8)
        self.eval(Mul(Lit(5), Neg(Lit(1))), -5)

        from interp import eval
        
        # Testing with float literals
        with self.assertRaises(EvalError) as context:
            eval(Mul(Lit(3.8), Lit(0.2)))
        self.assertEqual(str(context.exception), "multiplication operator requires integer operands")

        # Testing with boolean literals
        with self.assertRaises(EvalError) as context:
            eval(Mul(Lit(5), Lit(True)))
        self.assertEqual(str(context.exception), "cannot multiply boolean values")
        
        # Testing with string literals
        with self.assertRaises(EvalError) as context:
            eval(Mul(Lit("hello"), Lit(2)))
        self.assertEqual(str(context.exception), "multiplication operator requires integer operands")

    def test_Div(self):
        # Test division of two literals
        self.eval(Div(Add(Lit(4), Lit(2)), Lit(2)), 3)
        self.eval(Div(Lit(5), Lit(2)), 2)
        self.eval(Div(Lit(0), Lit(4)), 0)
        
        from interp import eval

        # Testing with float literals
        with self.assertRaises(EvalError) as context:
            eval(Div(Lit(20), Lit(2.5)))
        self.assertEqual(str(context.exception), "division operator requires integer operands")
        
        # Testing with Boolean literals
        with self.assertRaises(EvalError) as context:
            eval(Div(Lit(5), Lit(True)))
        self.assertEqual(str(context.exception), "cannot divide boolean values")
        
        # Testing with string literals
        with self.assertRaises(EvalError) as context:
            eval(Div(Lit("hello"), Lit(2)))
        self.assertEqual(str(context.exception), "division operator requires integer operands")
        
        # Testing division by zero
        with self.assertRaises(EvalError) as context:
            eval(Div(Lit(4), Lit(0)))
        self.assertEqual(str(context.exception), "division by zero")
        

    def test_Neg(self):
        # Test negation of a literal
        self.eval(Neg(Add(Lit(5), Lit(2))), -7)
        self.eval(Neg(Lit(-5)), 5)
        self.eval(Neg(Lit(5)), -5)
        self.eval(Neg(Lit(0)), 0)

        from interp import eval

        # Testing with float literals
        with self.assertRaises(EvalError) as context:
            eval(Neg(Lit(2.4)))
        self.assertEqual(str(context.exception), "negation operator requires integer operands")

        # Testing with boolean literals
        with self.assertRaises(EvalError) as context:
            eval(Neg(Lit(True)))
        self.assertEqual(str(context.exception), "cannot negate boolean values")
        
        # Testing with string literals
        with self.assertRaises(EvalError) as context:
            eval(Neg(Lit("hello")))
        self.assertEqual(str(context.exception), "negation operator requires integer operands")

    def test_And(self):
        # Test logical AND of two literals
        self.eval(And(Lit(True), Lit(True)), True)
        self.eval(And(Lit(True), Lit(False)), False)
        self.eval(And(Lit(False), Lit(True)), False)
        self.eval(And(Lit(False), Lit(False)), False)

        from interp import eval

        # Testing with float literals
        with self.assertRaises(EvalError) as context:
            eval(And(Lit(3.8), Lit(5)))
        self.assertEqual(str(context.exception), "And operator requires boolean operands")
        
        # Testing with string literals
        with self.assertRaises(EvalError) as context:
            eval(And(Lit("Hello"), Lit(True)))
        self.assertEqual(str(context.exception), "And operator requires boolean operands")

        # Testing with integer literals
        with self.assertRaises(EvalError) as context:
            eval(And(Lit(True), Lit(5)))
        self.assertEqual(str(context.exception), "And operator requires boolean operands")

    def test_Or(self):
        # Test logical OR of two literals
        self.eval(Or(Lit(True), Lit(True)), True)
        self.eval(Or(Lit(True), Lit(False)), True)
        self.eval(Or(Lit(False), Lit(True)), True)
        self.eval(Or(Lit(False), Lit(False)), False)

        from interp import eval

        # Testing with float literals
        with self.assertRaises(EvalError) as context:
            eval(Or(Lit(3.8), Lit(True)))
        self.assertEqual(str(context.exception), "Or operator requires boolean operands")
        
        # Testing with string literals
        with self.assertRaises(EvalError) as context:
            eval(Or(Lit("Hello"), Lit(False)))
        self.assertEqual(str(context.exception), "Or operator requires boolean operands")
        
        # Testing with integer literals
        with self.assertRaises(EvalError) as context:
            eval(Or(Lit(True), Lit(5)))
        self.assertEqual(str(context.exception), "Or operator requires boolean operands")

    def test_Not(self):
        # Test logical NOT of a literal
        self.eval(Not(Lit(True)), False)
        self.eval(Not(Lit(False)), True)

        from interp import eval

        # Testing with float literals
        with self.assertRaises(EvalError) as context:
            eval(Not(Lit(8.9)))
        self.assertEqual(str(context.exception), "Not operator requires boolean operands")
        
        # Testing with string literals
        with self.assertRaises(EvalError) as context:
            eval(Not(Lit("Hello")))
        self.assertEqual(str(context.exception), "Not operator requires boolean operands")
        
        # Testing with integer literals
        with self.assertRaises(EvalError) as context:
            eval(Not(Lit(5)))
        self.assertEqual(str(context.exception), "Not operator requires boolean operands")

    def test_Name(self):
        from interp import eval

        # Test evaluation of a name
        with self.assertRaises(EvalError) as context:
            eval(Name("x"))
        self.assertEqual(str(context.exception), "unbound Name: x")

    def test_Let(self):
        # Test evaluation of a let expression
        self.eval(Let("x", Add(Lit(1), Lit(2)), Sub(Name("x"), Lit(3))), 0)
        self.eval(Let("x", Lit(5), (Let("y", Lit(2), Add(Name("x"), Name("y"))))), 7)
        self.eval(Let("x", Lit(5), (Let("y", Lit(2), (Let("x", Lit(2), Add(Name("x"), Name("y"))))))), 4)
        self.eval(Let("x", Lit(5), Add(Name("x"), Lit(2))), 7)

        from interp import eval
        
        # Testing with empty name
        with self.assertRaises(EvalError) as context:
            eval(Let("", Lit(5), Add(Name("x"), Lit(2))))
        self.assertEqual(str(context.exception), "Name cannot be empty")