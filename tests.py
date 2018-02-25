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

    def test_gettoken_newline(self):
        from arithmetic import Lexer
        lexer = Lexer( ' \n ' )
        lexer.gettoken()
        self.assertEqual( lexer.value, '\n' )
        self.assertEqual( lexer.type, 'r' )

    def test_gettoken_f(self):
        from arithmetic import Lexer
        lexer = Lexer( ' 5 ' )
        lexer.gettoken()
        self.assertEqual( lexer.value, '5' )
        self.assertEqual( lexer.type, 'f' )

    def test_gettoken_x_enclosed(self):
        from arithmetic import Lexer
        lexer = Lexer( '5x3' )
        lexer.gettoken()
        lexer.gettoken()
        self.assertEqual( lexer.value, 'x' )
        self.assertEqual( lexer.type, 'x' )

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

    def test_gettoken_invalid(self):
        from arithmetic import Lexer
        lexer = Lexer( ' @ ' )
        lexer.gettoken()
        self.assertEqual( lexer.value, '@***' )
        self.assertEqual( lexer.type, 'u' )

class Evaluate( unittest.TestCase):

    def test_evaluate_factor(self):
        from arithmetic import evaluate
        res = evaluate('5*2')
        self.assertEqual( res, '10' )

    def test_evaluate_negative_factor(self):
        from arithmetic import evaluate
        res = evaluate('5*-2')
        self.assertEqual( res, '-10' )

    def test_evaluate_factor_percentage(self):
        from arithmetic import evaluate
        res = evaluate('50%')
        self.assertEqual( res, '0.5' )

    def test_evaluate_factor_open_parenthesis(self):
        from arithmetic import evaluate
        res = evaluate('(1)')
        self.assertEqual( res, '1' )

    def test_evaluate_factor_multiple_word_identifier(self):
        from arithmetic import evaluate
        res = evaluate('avg val', variables={'avg val':'5'})
        self.assertEqual( res, '5' )

    def test_evaluate_factor_name_undefined(self):
        from arithmetic import evaluate
        from decimal import InvalidOperation
        self.assertRaises( InvalidOperation, evaluate, 'a' )

    def test_evaluate_factors(self):
        from arithmetic import evaluate
        res = evaluate('5**2')
        self.assertEqual( res, '25' )

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


class TypeAndValueOf(unittest.TestCase):

    def test_v(self):
        from arithmetic import TypeAndValueOf
        res = TypeAndValueOf('')
        self.assertEqual( res, ('v', ''))

    def test_f(self):
        from arithmetic import TypeAndValueOf
        res = TypeAndValueOf('5.0')
        self.assertEqual( res, ('f', '5.0'))

    def test_n(self):
        from arithmetic import TypeAndValueOf
        res = TypeAndValueOf('name')
        self.assertEqual( res, ('n', 'name'))

    def test_e(self):
        from arithmetic import TypeAndValueOf
        res = TypeAndValueOf('name + 2')
        self.assertEqual( res, ('e', 'name + 2'))

    def test_a(self):
        from arithmetic import TypeAndValueOf
        res = TypeAndValueOf('2 + 2')
        self.assertEqual( res, ('a', '2 + 2'))


class FindLeftStarts(unittest.TestCase):

    def test_begin_of_line(self):
        from arithmetic import find_left_starts

        expected = [0, 0]
        result = find_left_starts('2+2 =', 0, 4, 5)
        self.assertEqual(expected, result)

    def test_spaces(self):
        from arithmetic import find_left_starts

        expected = [0, 5, 2]
        result = find_left_starts('  a  2+2 =', 0, 9, 10)
        self.assertEqual(expected, result)

    def test_colon(self):
        from arithmetic import find_left_starts

        expected = [0, 3, 0]
        result = find_left_starts('a: 2+2 =', 0, 7, 8)
        self.assertEqual(expected, result)

    def test_previous_equals_sign(self):
        from arithmetic import find_left_starts

        expected = [4, 0]
        result = find_left_starts('a = 2+2 =', 4, 8, 9)
        self.assertEqual(expected, result)


class FindRightEnds(unittest.TestCase):

    def test_separator(self):
        from arithmetic import find_right_ends

        match_eqs_next = None
        expected = [4, 4]
        result = find_right_ends('2+1=    ', 4, match_eqs_next)
        self.assertEqual(expected, result)

    def test_equals_sign_next(self):
        from unittest.mock import Mock
        from arithmetic import find_right_ends

        match_eqs_next = Mock()
        match_eqs_next.start.return_value = 10
        expected = [10, 4, 11]
        result = find_right_ends('2+1=      =', 4, match_eqs_next)
        self.assertEqual(expected, result)

    def test_end_of_line(self):
        from arithmetic import find_right_ends

        match_eqs_next = None
        expected = [4]
        result = find_right_ends('2+1=', 4, match_eqs_next)
        self.assertEqual(expected, result)


class Parser(unittest.TestCase):

    def test_instance(self):
        from arithmetic import Parser
        self.assertIsInstance( Parser(), Parser )

    def test_parse(self):
        from arithmetic import Parser
        parser = Parser()
        self.assertEqual( parser.parse('2+2='), '2+2=4' )

    def test_parseLine_mSeparLeft(self):
        from arithmetic import Parser
        parser = Parser()
        lines = ['  a  2+2 =']
        parser.parseLine(0, lines)
        self.assertEqual( lines[0], '  a  2+2 =4' )

    def test_parseLine_mColonLeft(self):
        from arithmetic import Parser
        parser = Parser()
        lines = ['a: 2+2 =']
        parser.parseLine(0, lines)
        self.assertEqual( lines[0], 'a: 2+2 =4' )

    def test_parseLine_mEqualSignNext(self):
        from arithmetic import Parser
        parser = Parser()
        lines = ['a: 2+2 =   2x3=']
        parser.parseLine(0, lines)
        self.assertEqual( lines[0], 'a: 2+2 = 4  2x3=6' )


class ParserParseLine(unittest.TestCase):


    def setUp(self):
        from unittest.mock import Mock
        import arithmetic

        arithmetic.print = Mock()

    def tearDown(self):
        import arithmetic

        del arithmetic.print

    def test_evaluate_expression(self):
        import arithmetic

        parser = arithmetic.Parser()
        lines = ['a + 1 =']
        parser.parseLine(0, lines)
        arithmetic.print.assert_called_with('eval error:', 'e' , 'a + 1', 'v', '')

    def test_assign_to_variable(self):
        import arithmetic

        parser = arithmetic.Parser()
        lines = ['a=1']
        variables = {}
        parser.parseLine(0, lines, variables=variables)
        self.assertEqual(variables, {'a': '1'})

    def test_assign_to_variable_exception(self):
        import arithmetic
        import decimal

        parser = arithmetic.Parser()
        lines = ['a=1/0']
        self.assertRaises(decimal.DivisionByZero, parser.parseLine, 0, lines)

    def test_evaluate_variable(self):
        import arithmetic

        parser = arithmetic.Parser()
        lines = ['a=']
        variables = {'a': '1'}
        parser.parseLine(0, lines, variables=variables)
        self.assertEqual(lines, ['a=1'])

    def test_evaluate_function(self):
        import arithmetic

        parser = arithmetic.Parser()
        lines = ['f=']
        variables = {'a': '1'}
        functions = {'f': 'a+1'}
        parser.parseLine(0, lines, variables=variables, functions=functions)
        self.assertEqual(lines, ['f=2'])

    def test_evaluate_function_exception(self):
        import arithmetic

        parser = arithmetic.Parser()
        lines = ['f=']
        functions = {'f': 'a+1'}
        parser.parseLine(0, lines, functions=functions)
        arithmetic.print.assert_called_with('eval error:', 'n', 'f', 'v', '')

    def test_function_recursive_initial_value(self):
        import arithmetic

        parser = arithmetic.Parser()
        lines = ['f=1']
        variables = {}
        functions = {'f': 'f+3'}
        parser.parseLine(0, lines, variables=variables, functions=functions)
        self.assertEqual(variables, {'f': '1'})

    def test_function_recursive_iteration(self):
        import arithmetic

        parser = arithmetic.Parser()
        lines = ['f=']
        variables = {'f': '1'}
        functions = {'f': 'f+3'}
        parser.parseLine(0, lines, variables=variables, functions=functions)
        self.assertEqual(variables, {'f': '4'})

    def test_define_function(self):
        import arithmetic

        parser = arithmetic.Parser()
        lines = ['a=f+1']
        functions = {}
        parser.parseLine(0, lines, functions=functions)
        self.assertEqual(functions, {'a': 'f+1'})

    def test_define_an_alias(self):
        import arithmetic

        parser = arithmetic.Parser()
        lines = ['a=b']
        functions = {}
        parser.parseLine(0, lines, functions=functions)
        self.assertEqual(functions, {'a': 'b'})


class AddCommas(unittest.TestCase):

    def test_commas(self):
        from arithmetic import AddCommas

        self.assertEqual('1,000', AddCommas(1000))


if __name__ == '__main__':
    unittest.main()

