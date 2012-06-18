import unittest

class Lexer( unittest.TestCase):

    def test_instance(self):
        from arithmetic import Lexer
        lexer = Lexer( '5x3 ' )
        self.assertEqual( lexer.text, '5x3 ' )
        self.assertEqual( lexer.offset, 0 )

    def test_gettoken_null_text(self):
        from arithmetic import Lexer
        lexer = Lexer( '' )
        lexer.gettoken()
        self.assertEqual( lexer.value, None )
        self.assertEqual( lexer.type, '' )

    def test_gettoken_f(self):
        from arithmetic import Lexer
        lexer = Lexer( ' 5 ' )
        lexer.gettoken()
        self.assertEqual( lexer.value, '5' )
        self.assertEqual( lexer.type, 'f' )

    def test_gettoken_n(self):
        from arithmetic import Lexer
        lexer = Lexer( ' name ' )
        lexer.gettoken()
        self.assertEqual( lexer.value, 'name' )
        self.assertEqual( lexer.type, 'n' )

    def test_gettoken_power(self):
        from arithmetic import Lexer
        lexer = Lexer( ' ** ' )
        lexer.gettoken()
        self.assertEqual( lexer.value, '**' )
        self.assertEqual( lexer.type, 'o' )

    def test_gettoken_plus(self):
        from arithmetic import Lexer
        lexer = Lexer( ' + ' )
        lexer.gettoken()
        self.assertEqual( lexer.value, '+' )
        self.assertEqual( lexer.type, 'o' )

class Evaluate( unittest.TestCase):

    def test_evaluate_numeric(self):
        from arithmetic import evaluate
        res = evaluate('5+2')
        self.assertEqual( res, '7' )

    def test_evaluate_variable(self):
        from arithmetic import evaluate
        res = evaluate('a', variables={'a':'1'})
        self.assertEqual( res, '1' )

    def test_evaluate_variable_plus(self):
        from arithmetic import evaluate
        res = evaluate('f+1', variables={'f':'1'})
        self.assertEqual( res, '2' )

    def test_evaluate_function(self):
        from arithmetic import evaluate
        res = evaluate('f', variables={'a':'1'}, functions={'f': 'a+1'})
        self.assertEqual( res, '2' )

    def test_evaluate_function_name_substring(self):
        from arithmetic import evaluate
        res = evaluate('f', variables={'af':'1'}, functions={'f': 'af'})
        self.assertEqual( res, '1' )

    def test_evaluate_function_recursive_no_initial_value(self):
        from arithmetic import evaluate
        res = evaluate('f', functions={'f': 'f+1'})
        self.assertEqual( res, '0' )

if __name__ == '__main__':
    unittest.main()

