
#   Copyright (c) 2010 Patricio Paez <pp@pp.com.mx>
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

import re

# Written by the equation processor, read by evaluate():
variables = {}
functions = {}


renumber = re.compile( r'([0-9][0-9,]*(\.[0-9]*)?%?)|(\.[0-9]+%?)' )
reidentifier = re.compile( r'[a-zA-Z][a-zA-Z0-9_]*' )
rexenclosed = re.compile( r'[0-9.](x)[^a-zA-Z]' )

def gettoken( doc ):
    '''Get next token from text and return it.
    
    Return None if no more text.
    
    doc has text and offset attributes.

    Identifiers    letter ( letter | digit | _ )*
    Numbers        digit ( digit | , | . ) *
    Operators      - + * / ^ ** x
    
    x can be a name or an operator

    x preceeded and followed by a digit is taken as if
    preceeded and followed by a space.  i.e 5x3
    is seen as 5 x 3.
    '''
    while doc.offset < len( doc.text ):
        if doc.text[ doc.offset ] == ' ':
            value = doc.text[ doc.offset ]
            doc.offset = doc.offset + 1
            continue
        if doc.text[ doc.offset ] == '\n':
            value = doc.text[ doc.offset ]
            doc.offset = doc.offset + 1
            return value
        m = rexenclosed.match( doc.text, doc.offset - 1 )
        if m:
            value = m.group(1)
            doc.offset = m.end(1)
            return value
        m = renumber.match( doc.text, doc.offset )
        if m:
            value = m.group()
            doc.offset = m.end()
            return value
        m = reidentifier.match( doc.text, doc.offset )
        if m:
            value = m.group()
            doc.offset = m.end()
            return value
        if doc.text[ doc.offset: doc.offset + 2 ] == '**':
            value = doc.text[ doc.offset: doc.offset + 2 ]
            doc.offset = doc.offset + 2
            return value
        if doc.text[ doc.offset ] in '+-*/^()':
            value = doc.text[ doc.offset ]
            doc.offset = doc.offset + 1
            return value
        value = doc.text[ doc.offset ] + '***' 
        doc.offset = doc.offset + 1
        return value
    return None	


t = ''
from decimal import Decimal, getcontext
getcontext().prec = 100

def evaluate( expression_text ):
    '''Parse expression, calculate and return its result.

    '''
    global text
    global t
    tokens = []
    expression = []

    class doc:
        text = expression_text
        offset = 0

    def factor():
        global t
        if t in '-+':
            expression.append( t )
            t = gettoken( doc )
        if re.search( '[0-9]+', t ) :
            expression.append( t )
            t = gettoken( doc )
        elif t == '(':
            expression.append( t )
            t = gettoken( doc )
            expr()
            expression.append( t )
            t = gettoken( doc )
        elif re.search( '[a-zA-Z]+', t):
            if variables.has_key( t ):
                expression.append( variables[ t ] )
                t = gettoken( doc )
            elif functions.has_key( t ):
                expression.append( str( evaluate( functions[ t ] ) ) )
                t = gettoken( doc )
            else:
                expression.append( t + ' undefined' )
                t = gettoken( doc )

    def factors():
        global t
        if t == '^' or t == '**':
            expression.append( '**' )
            t = gettoken( doc )
            power()

    def power():
        factor()
        factors()

    def powers():
        global t
        if t and t in '*x/':
            expression.append( t.replace( 'x', '*') )
            t = gettoken( doc )
            power()
            powers()

    def term():
        power()
        powers()

    def terms():
        global t
        if t and t in '-+':
            expression.append( t )
            t = gettoken( doc )
            term()
            terms()

    def expr():
        term()
        terms()

    t = gettoken( doc )
    expr()

    expressionD = []
    for element in expression:
        if element not in '+-x/^*()' or element == '**':
            element = "Decimal('" + element + "')"
        expressionD.append( element )

    return eval( ''.join( expressionD ) )



reEqualSign = re.compile( ' ?= ?' )
reSepar = re.compile( '  +' )
reColonLeft = re.compile( ': ' )

globales = { '__builtins__' : '' }
funciones = []


def TypeAndValueOf( expression ):
    '''"Returns a (type, value) tuple.
    
    type may be:
    
    v = void
    i = integer, f = float
    e = expression containing variables
    a = arithmetic expression, no variables
    n = name
    
    value is expression with some modifications:
    blank spaces and commas removed, x replaced by *,
    % replaced by /100.'''

    if not expression.strip():  # empty
        return 'v', ''
    try:
        n = int( expression.replace( ',', '' ) )
        return 'i', n
    except:
        try:
            n = float( expression.replace( ',', '' ) )
            return 'f', n
        except:
            expresion_python = re.sub( r'\bx\b', '*', expression )
            expresion_python = re.sub( r'%', '/100.', expresion_python )
            for op in '+-*/':
                if op in expresion_python:
                    expresion_python = expresion_python.replace( ' ', '' )
                    if re.search( '([a-zA-Z][a-zA-Z0-9]*)', expresion_python ):
                        return 'e', expresion_python  # expression with names
                    return 'a', expresion_python
            return 'n', expression.replace( ' ', '' )

def feed( text ):
    'Feed text to the parser.  It is processed line by line.'

    global functions, variables
    # Initialize
    functions = {}
    variables = {}

    lines = []

    for linenumber, line in enumerate( text.splitlines() ):

        RightPrevStart = 0
        RightPrevEnd = 0
        mEqualSignPrev = re.search( '^', line )
        mEqualSignAct = reEqualSign.search( line, mEqualSignPrev.end() )
        while mEqualSignAct:

            # Determine LeftActStart,
            # the larger of mEqualSignPrev, mSeparLeft, mColonLeft, beginofline
            LeftStarts = []
            LeftStarts.append( mEqualSignPrev.end() )
            mSeparLeft = reSepar.search( line, mEqualSignPrev.end(), mEqualSignAct.start() )
            if mSeparLeft:
                LeftStarts.append( mSeparLeft.end() )
            mColonLeft = reColonLeft.search( line, mEqualSignPrev.end(), mEqualSignAct.start() )
            if mColonLeft:
                LeftStarts.append( mColonLeft.end() )
            mBeginOfLine = re.search( '^ *', line )
            LeftStarts.append( mBeginOfLine.end() )
            LeftActStart = max( LeftStarts )

            # Determine RightActEnd,
            # the smaller of mEqualSignNext, mSeparRight, endofline
            RightEnds = []
            mEqualSignNext = reEqualSign.search( line, mEqualSignAct.end() )
            if mEqualSignNext:
                RightEnds.append( mEqualSignNext.start() )
            mSeparRight = reSepar.search( line, mEqualSignAct.end() )
            if mSeparRight:
                RightEnds.append( mSeparRight.start() )
            mEndOfLine = re.search( ' *$', line )
            RightEnds.append( mEndOfLine.start() )
            RightActEnd = min( RightEnds )

            rangolibre   = line[ RightPrevEnd          : LeftActStart ]
            rangoLeft    = line[ LeftActStart          : mEqualSignAct.start() ]
            rangocentro  = line[ mEqualSignAct.start() : mEqualSignAct.end() ]
            rangoRight   = line[ mEqualSignAct.end()   : RightActEnd ]

            tipoLeft, valorLeft = TypeAndValueOf( rangoLeft )
            tipoRight, valorRight = TypeAndValueOf( rangoRight )

            if tipoLeft != 'v': # there is something to the left

                # perform operations

                if tipoLeft in 'ea' and tipoRight in 'vif':# evaluate expression
                    try:
                        resultado = str( evaluate( valorLeft ) )
                        line = writeResult( line, mEqualSignAct.end(), RightActEnd, resultado )
                    except:
                        print 'eval error:', tipoLeft, valorLeft, tipoRight, valorRight
                elif tipoLeft == 'n' and tipoRight in 'ifav':
                    if valorLeft not in functions:     # variable on the left
                        if tipoRight != 'v':    # assign to variable
                            try:
                                variables[ valorLeft ] = str( evaluate( str( valorRight) ) )

                            except:
                                print 'exec error:', tipoLeft, valorLeft, tipoRight, valorRight
                                raise
                        else:                   # evaluate a variable
                            if valorLeft in variables:
                                    resultado = variables[ valorLeft ]
                                    line = writeResult( line, mEqualSignAct.end(), RightActEnd, resultado )

                    else:                                  # function on the left: evaluate
                        if valorLeft not in functions[ valorLeft ]:
                            try:                # standard formula
                                resultado = str( evaluate( valorLeft ) )
                                line = writeResult( line, mEqualSignAct.end(), RightActEnd, resultado )
                            except:
                                print 'eval error:', tipoLeft, valorLeft, tipoRight, valorRight
                        else:                   # recurrence relation
                            if valorLeft not in variables:            # initial value
                              if valorRight != '':
                                variables[ valorLeft ] = str( evaluate( str( valorRight ) ) )
                            else:                                         # iteration
                                resultado = str( evaluate( functions[ valorLeft ] ) )
                                line = writeResult( line, mEqualSignAct.end(), RightActEnd, resultado )
                                variables[ valorLeft ] = resultado

                elif tipoLeft == 'n' and tipoRight in 'e': # define a function
                        functions[ valorLeft ] = str(valorRight)

                elif tipoLeft == 'n' and tipoRight in 'n': # define an alias
                        functions[ valorLeft ] = str(valorRight)



                RightPrevStart = mEqualSignAct.end()
                RightPrevEnd = RightActEnd

            if mEqualSignNext:
                mEqualSignNext = reEqualSign.search( line, mEqualSignAct.end() )
            mEqualSignPrev = mEqualSignAct
            mEqualSignAct  = mEqualSignNext

        lines.append( line )

    return '\n'.join( lines )


def writeResult( buffer, start, end, text ):
    'Return buffer with text applied from start to end offset.'

    return buffer[ :start ] + text + buffer[ end: ]


if __name__ == '__main__':
    import sys
    text = open( sys.argv[1] ).read()
    print feed( text )
