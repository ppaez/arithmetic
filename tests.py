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

if __name__ == '__main__':
    unittest.main()

