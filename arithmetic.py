
#   Copyright (c) 2010, 2011 Patricio Paez <pp@pp.com.mx>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>


__doc__ = '''
arithmetic is a Python module that allows mixing arithmetic
operations and text.

Usage as command:

      arithmetic expression(s) Evaluate expression(s).
      arithmetic -f path       Read path contents and evaluate.
      arithmetic               Read from standard input and evaluate.
      arithmetic -h            Show usage

Examples:

      $ arithmetic 2 x 3
      6
      $ echo 4 x 12 | arithmetic
      48
      $ echo 'a = 5    a + 4 =' | arithmetic
      a = 5    a + 4 = 9
      $ arithmetic < filename
      ...

Usage as module:

     from arithmetic import Parser
     ...
     parser = Parser()
     resultText = parser.parse(inputText)
     ...
'''

import re


renumber = re.compile( r'([0-9][0-9,]*(\.[0-9]*)?%?)|(\.[0-9]+%?)' )
reidentifier = re.compile( r'[a-zA-Z][a-zA-Z0-9_]*' )
rexenclosed = re.compile( r'[0-9.)](x)[^a-zA-Z]' )

class Lexer:
    ''
    def __init__( self, text ):
        self.text = text
        self.offset = 0

    def gettoken( self ):
        '''Get next token from text and return its type and value.

        Return (None,None) if no more text.

        Identifiers    letter ( letter | digit | _ )*
        Numbers        digit ( digit | , | . ) *
        Operators      - + * / ^ ** x

        x can be a name or an operator

        x preceeded and followed by a digit is taken as if
        preceeded and followed by a space.  i.e 5x3
        is seen as 5 x 3.
        '''
        while self.offset < len( self.text ):
            if self.text[ self.offset ] == ' ':
                value = self.text[ self.offset ]
                self.offset = self.offset + 1
                continue
            if self.text[ self.offset ] == '\n':
                value = self.text[ self.offset ]
                self.offset = self.offset + 1
                self.type = 'r'
                self.value = value
                return
            m = renumber.match( self.text, self.offset )
            if m:
                value = m.group()
                self.offset = m.end()
                self.type = 'f'
                self.value = value
                return
            m = rexenclosed.match( self.text, self.offset - 1 )
            if m:
                value = m.group(1)
                self.offset = m.end(1)
                self.type = 'x'
                self.value = value
                return
            m = reidentifier.match( self.text, self.offset )
            if m:
                value = m.group()
                self.offset = m.end()
                self.type = 'n'
                self.value = value
                return
            if self.text[ self.offset: self.offset + 2 ] == '**':
                value = self.text[ self.offset: self.offset + 2 ]
                self.offset = self.offset + 2
                self.type = 'o'
                self.value = value
                return
            if self.text[ self.offset ] in '+-*/^()':
                value = self.text[ self.offset ]
                self.offset = self.offset + 1
                self.type = 'o'
                self.value = value
                return
            value = self.text[ self.offset ] + '***'
            self.offset = self.offset + 1
            self.type = 'u'
            self.value = value
            return
        self.type = ''
        self.value = None


from decimal import Decimal, getcontext
getcontext().prec = 100

def find(name, formula):
    'Return True or False if name is used or not in formula'
    return re.search( r'\b'+name+r'\b', formula)

def evaluate( expression_text, UseDigitGrouping = True, variables = {}, functions = {} ):
    '''Parse expression, calculate and return its result.

    if UseDigitGrouping is True, the result includes commas.

    '''
    expression = []

    lexer = Lexer( expression_text )

    def factor():
        if lexer.value in '-+':
            expression.append( lexer.value )
            lexer.gettoken()
        if lexer.type == 'f':
            #  remove commas and spaces
            #  translate % to /100'''
            value = lexer.value.replace( '%', '' )
            value = value.replace( ' ', '' )
            expression.append( value.replace( ',', '' ) )
            if lexer.value[-1] == '%':
                expression.append( '/' )
                expression.append( '100' )
            lexer.gettoken()
        elif lexer.value == '(':
            expression.append( lexer.value )
            lexer.gettoken()
            expr()
            expression.append( lexer.value )
            lexer.gettoken()
        elif lexer.type == 'n':
            name = lexer.value
            lexer.gettoken()
            # handle multiple word names
            while lexer.type == 'n' and lexer.value != 'x':
                name = name + ' ' + lexer.value
                lexer.gettoken()
            if name in variables:
                # remove commas
                value = variables[ name ].replace( ',', '' )
                expression.append( value )
            elif name in functions:
                if not find( name, functions[ name ]):
                    # standard formula
                    expression.append( str( evaluate( functions[ name ],
                                       UseDigitGrouping = False,
                                       variables=variables, functions=functions ) ) )
                else:
                    # recurrent relation wihout initial value
                    expression.append( '0' )
            else:
                expression.append( name + ' undefined' )

    def factors():
        if lexer.value == '^' or lexer.value == '**':
            expression.append( '**' )
            lexer.gettoken()
            power()

    def power():
        factor()
        factors()

    def powers():
        if lexer.value and lexer.value in '*x/':
            expression.append( lexer.value.replace( 'x', '*') )
            lexer.gettoken()
            power()
            powers()

    def term():
        power()
        powers()

    def terms():
        if lexer.value and lexer.value in '-+':
            expression.append( lexer.value )
            lexer.gettoken()
            term()
            terms()

    def expr():
        term()
        terms()

    lexer.gettoken()
    expr()

    expressionD = []
    for element in expression:
        if element not in '+-x/^*()' and element != '**':
            element = "Decimal('" + element + "')"
        expressionD.append( element )

    if UseDigitGrouping:
        return AddCommas( eval( ''.join( expressionD ) ) )
    else:
        return eval( ''.join( expressionD ) )



reEqualSign = re.compile( ' ?= ?' )
reSepar = re.compile( '  +' )
reColonLeft = re.compile( ': ' )



def TypeAndValueOf( expression ):
    '''"Returns a (type, value) tuple.
    
    type may be:
    
    v = void
    i = integer, f = float
    e = expression containing variables
    a = arithmetic expression, no variables
    n = name
    
    value is expression with some modifications:
    blank spaces and commas removed, x replaced by *.'''

    lexer = Lexer( expression )

    # Capture the odd token types
    lexer.text = re.sub( '[()]', '', lexer.text )
    lexer.gettoken()
    oddtokens = lexer.type
    while lexer.type:
        lexer.gettoken()
        lexer.gettoken()
        oddtokens = oddtokens + lexer.type

    if oddtokens == '':  # empty
        return 'v', ''
    elif oddtokens == 'f':
        return 'f', expression
    elif oddtokens == 'n':
        return 'n', expression
    elif 'n' in oddtokens or 'x' in oddtokens:
        return 'e', expression  # expression with names
    else:
        return 'a', expression


def find_left_starts(line, eqs_prev, eqs_start, eqs_end):
    'return the larger of eqs_prev, mSeparLeft, mColonLeft, beginofline'

    LeftStarts = []
    LeftStarts.append(eqs_prev)

    mSeparLeft = reSepar.search(line, eqs_prev, eqs_start)
    if mSeparLeft:
        SeparLeftEnd = mSeparLeft.end()
        mSeparLeft = reSepar.search( line, mSeparLeft.end(), eqs_start)
        while mSeparLeft:     # search next
            SeparLeftEnd = mSeparLeft.end()
            mSeparLeft = reSepar.search( line, mSeparLeft.end(), eqs_start)
        LeftStarts.append( SeparLeftEnd )

    mColonLeft = reColonLeft.search(line, eqs_prev, eqs_start)
    if mColonLeft:
        LeftStarts.append( mColonLeft.end() )
    mBeginOfLine = re.search( '^ *', line )
    LeftStarts.append( mBeginOfLine.end() )
    return LeftStarts


def find_right_ends(line, eqs_end, mEqualSignNext):
    'return the smaller of mEqualSignNext, mSeparRight, endofline'

    RightEnds = []
    if mEqualSignNext:
        RightEnds.append( mEqualSignNext.start() )
    mSeparRight = reSepar.search( line, eqs_end)
    if mSeparRight:
        RightEnds.append( mSeparRight.start() )
    mEndOfLine = re.search( ' *$', line )
    RightEnds.append( mEndOfLine.start() )
    return RightEnds


def perform_operations(lhs_type, lhs_value, rhs_type, rhs_value,
                       variables, functions,
                       writeResult, rhs_start, rhs_end, lines, i):
    'perform operations, call writeResult as needed'

    if lhs_type in 'eaif' and rhs_type in 'vif':# evaluate expression
        try:
            resultado = str( evaluate(lhs_value,
                        variables=variables, functions=functions ) )
            writeResult(i, lines, rhs_start, rhs_end, resultado)
        except:
            print('eval error:', lhs_type, lhs_value, rhs_type, rhs_value)
    elif lhs_type == 'n' and rhs_type in 'ifav':
        if lhs_value not in functions:     # variable on the left
            if rhs_type != 'v':    # assign to variable
                try:
                    variables[lhs_value] = str(evaluate(str(rhs_value),
                                            variables=variables, functions=functions ) )

                except:
                    print('exec error:', lhs_type, lhs_value, rhs_type, rhs_value)
                    raise
            else:                   # evaluate a variable
                if lhs_value in variables:
                        resultado = variables[lhs_value]
                        resultado = AddCommas( resultado )
                        writeResult(i, lines, rhs_start, rhs_end, resultado)

        else:                                  # function on the left: evaluate
            if not find(lhs_value, functions[lhs_value]):
                try:                # standard formula
                    resultado = str(evaluate(lhs_value,
                                variables=variables, functions=functions ) )
                    writeResult(i, lines, rhs_start, rhs_end, resultado)
                except:
                    print('eval error:', lhs_type, lhs_value, rhs_type, rhs_value)
            else:                   # recurrence relation
                if lhs_value not in variables:            # initial value
                  if rhs_value != '':
                    variables[lhs_value] = str(evaluate(str(rhs_value),
                                            variables=variables, functions=functions ) )
                else:                                         # iteration
                    resultado = str( evaluate( functions[lhs_value],
                                    variables=variables, functions=functions ) )
                    writeResult(i, lines, rhs_start, rhs_end, resultado)
                    variables[lhs_value] = resultado

    elif lhs_type == 'n' and rhs_type in 'e': # define a function
            functions[lhs_value] = str(rhs_value)

    elif lhs_type == 'n' and rhs_type in 'n': # define an alias
            functions[lhs_value] = str(rhs_value)


class Parser:
    'Base class'

    def __init__( self ):
        # Written by parseLine(), read by evaluate():
        self.functions = {}
        self.variables = {}

    def parse( self, text ):
        'Find expresions in text, return it with results.'

        lines = text.splitlines()

        for i in range( self.countLines( lines ) ):
            self.parseLine( i, lines, variables=self.variables, functions=self.functions )

        return '\n'.join( lines )

    def countLines( self, lines ):
        'Return number of lines.'
        return len( lines )

    def readLine( self, i, lines ):
        'Return i line from lines.'
        return lines[i]

    def writeResult( self, i, lines, start, end, text ):
        'Write text in line i of lines from start to end offset.'

        lines[i] = lines[i][ :start ] + text + lines[i][ end: ]

    def parseLine( self, i, lines, variables={}, functions={} ):
            'Find and evaluate expresions in line i.'

            # get line
            line = self.readLine( i, lines )

            RightPrevStart = 0
            RightPrevEnd = 0
            eqs_prev = 0
            mEqualSignAct = reEqualSign.search(line, eqs_prev)
            while mEqualSignAct:
                eqs_start = mEqualSignAct.start()
                eqs_end = mEqualSignAct.end()
                mEqualSignNext = reEqualSign.search( line, eqs_end)

                LeftStarts = find_left_starts(line, eqs_prev, eqs_start, eqs_end)
                lhs_start = max(LeftStarts)

                RightEnds = find_right_ends(line, eqs_end, mEqualSignNext)
                rhs_end = min(RightEnds)

                lhs = line[lhs_start:eqs_start]
                rhs = line[eqs_end:rhs_end]

                lhs_type, lhs_value = TypeAndValueOf(lhs)
                rhs_type, rhs_value = TypeAndValueOf(rhs)

                if lhs_type != 'v': # there is something to the left
                    perform_operations(lhs_type, lhs_value, rhs_type, rhs_value,
                                       variables, functions, self.writeResult,
                                       eqs_end, rhs_end, lines, i)
                    RightPrevStart = eqs_end
                    RightPrevEnd = rhs_end

                # get line
                line = self.readLine( i, lines )

                if mEqualSignNext:
                    mEqualSignNext = reEqualSign.search( line, eqs_end)
                eqs_prev = eqs_end
                mEqualSignAct  = mEqualSignNext


def AddCommas( s ):
    ''''Return s with thousands separators.

    Handles sign, decimals and thousands
    separator.
    '''

    s = str( s )
    s = s.replace( ',', '')         #remove commas
    if s[0] in '-+':                #remove sign
            sign = s[0]
            s = s[1:]
    else:
            sign = ''
    if s[-1] == 'L': s = s[:-1]     #remove L suffix
    pos = s.find( '.')
    if pos < 0: pos = len(s)
    while pos > 3:
            pos = pos - 3
            s = s[:pos] + ',' + s[pos:]
    s = sign + s                    #restore sign
    return s

