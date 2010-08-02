
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
rexenclosed = re.compile( r'[0-9.)](x)[^a-zA-Z]' )

def gettoken( doc ):
    '''Get next token from text and return its type and value.
    
    Return (None,None) if no more text.
    
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
            return ( 'r', value )
        m = renumber.match( doc.text, doc.offset )
        if m:
            value = m.group()
            doc.offset = m.end()
            return ( 'f', value )
        m = rexenclosed.match( doc.text, doc.offset - 1 )
        if m:
            value = m.group(1)
            doc.offset = m.end(1)
            return ( 'x', value )
        m = reidentifier.match( doc.text, doc.offset )
        if m:
            value = m.group()
            doc.offset = m.end()
            return ( 'n', value )
        if doc.text[ doc.offset: doc.offset + 2 ] == '**':
            value = doc.text[ doc.offset: doc.offset + 2 ]
            doc.offset = doc.offset + 2
            return ( 'o', value )
        if doc.text[ doc.offset ] in '+-*/^()':
            value = doc.text[ doc.offset ]
            doc.offset = doc.offset + 1
            return ( 'o', value )
        value = doc.text[ doc.offset ] + '***' 
        doc.offset = doc.offset + 1
        return ( 'u', value )
    return ( '', None )


t = ''
v = ''
from decimal import Decimal, getcontext
getcontext().prec = 100

def evaluate( expression_text ):
    '''Parse expression, calculate and return its result.

    '''
    global text
    global t, v
    tokens = []
    expression = []

    class doc:
        text = expression_text
        offset = 0

    def factor():
        global t, v
        if v in '-+':
            expression.append( v )
            t, v = gettoken( doc )
        if t == 'f':
            #  remove comas and spaces
            #  translate % to /100'''
            value = v.replace( '%', '' )
            value = value.replace( ' ', '' )
            expression.append( value.replace( ',', '' ) )
            if v[-1] == '%':
                expression.append( '/' )
                expression.append( '100' )
            t, v = gettoken( doc )
        elif v == '(':
            expression.append( v )
            t, v = gettoken( doc )
            expr()
            expression.append( v )
            t, v = gettoken( doc )
        elif t == 'n':
            name = v
            t, v = gettoken( doc )
            # handle multiple word names
            while t == 'n' and v != 'x':
                name = name + ' ' + v
                t, v = gettoken( doc )
            if name in variables:
                expression.append( variables[ name ] )
            elif name in functions:
                if name not in functions[ name ]:
                    # standard formula
                    expression.append( str( evaluate( functions[ name ] ) ) )
                else:
                    # recurrent relation wihout initial value
                    expression.append( '0' )
            else:
                expression.append( name + ' undefined' )

    def factors():
        global t, v
        if v == '^' or v == '**':
            expression.append( '**' )
            t, v = gettoken( doc )
            power()

    def power():
        factor()
        factors()

    def powers():
        global t, v
        if v and v in '*x/':
            expression.append( v.replace( 'x', '*') )
            t, v = gettoken( doc )
            power()
            powers()

    def term():
        power()
        powers()

    def terms():
        global t, v
        if v and v in '-+':
            expression.append( v )
            t, v = gettoken( doc )
            term()
            terms()

    def expr():
        term()
        terms()

    t, v = gettoken( doc )
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
    blank spaces and commas removed, x replaced by *.'''

    class doc:
        text = expression
        offset = 0

    # Capture the odd token types
    doc.text = re.sub( '[()]', '', doc.text )
    t, v = gettoken( doc )
    oddtokens = t
    while t:
        t, v = gettoken( doc )
        t, v = gettoken( doc )
        oddtokens = oddtokens + t

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
                SeparLeftEnd = mSeparLeft.end()
                mSeparLeft = reSepar.search( line, mSeparLeft.end(), mEqualSignAct.start() )
                while mSeparLeft:     # search next
                    SeparLeftEnd = mSeparLeft.end()
                    mSeparLeft = reSepar.search( line, mSeparLeft.end(), mEqualSignAct.start() )
                LeftStarts.append( SeparLeftEnd )

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

                if tipoLeft in 'eaif' and tipoRight in 'vif':# evaluate expression
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
