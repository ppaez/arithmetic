import re, aee

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

    # Initialize
    aee.functions = {}
    aee.variables = {}

    lines = []

    for linenumber, linea in enumerate( text.splitlines() ):

        RightPrevStart = 0
        RightPrevEnd = 0
        mEqualSignPrev = re.search( '^', linea )
        mEqualSignAct = reEqualSign.search( linea, mEqualSignPrev.end() )
        while mEqualSignAct:

            # Determine LeftActStart,
            # the larger of mEqualSignPrev, mSeparLeft, mColonLeft, beginofline
            LeftStarts = []
            LeftStarts.append( mEqualSignPrev.end() )
            mSeparLeft = reSepar.search( linea, mEqualSignPrev.end(), mEqualSignAct.start() )
            if mSeparLeft:
                LeftStarts.append( mSeparLeft.end() )
            mColonLeft = reColonLeft.search( linea, mEqualSignPrev.end(), mEqualSignAct.start() )
            if mColonLeft:
                LeftStarts.append( mColonLeft.end() )
            mBeginOfLine = re.search( '^ *', linea )
            LeftStarts.append( mBeginOfLine.end() )
            LeftActStart = max( LeftStarts )

            # Determine RightActEnd,
            # the smaller of mEqualSignNext, mSeparRight, endofline
            RightEnds = []
            mEqualSignNext = reEqualSign.search( linea, mEqualSignAct.end() )
            if mEqualSignNext:
                RightEnds.append( mEqualSignNext.start() )
            mSeparRight = reSepar.search( linea, mEqualSignAct.end() )
            if mSeparRight:
                RightEnds.append( mSeparRight.start() )
            mEndOfLine = re.search( ' *$', linea )
            RightEnds.append( mEndOfLine.start() )
            RightActEnd = min( RightEnds )

            rangolibre   = linea[ RightPrevEnd          : LeftActStart ]
            rangoLeft    = linea[ LeftActStart          : mEqualSignAct.start() ]
            rangocentro  = linea[ mEqualSignAct.start() : mEqualSignAct.end() ]
            rangoRight   = linea[ mEqualSignAct.end()   : RightActEnd ]

            tipoLeft, valorLeft = TypeAndValueOf( rangoLeft )
            tipoRight, valorRight = TypeAndValueOf( rangoRight )

            if tipoLeft != 'v': # there is something to the left

                # perform operations

                if tipoLeft in 'ea' and tipoRight in 'vif':# evaluate expression
                    try:
                        resultado = str( aee.evaluate( valorLeft ) )
                        linea = writeResult( linea, mEqualSignAct.end(), RightActEnd, resultado )
                    except:
                        print 'eval error:', tipoLeft, valorLeft, tipoRight, valorRight
                elif tipoLeft == 'n' and tipoRight == 'vNO' \
                        and valorLeft in aee.variables:    # evaluate variable or function
                    try: 
                        resultado = str( aee.evaluate( valorLeft ) )
                        linea = writeResult( linea, mEqualSignAct.end(), RightActEnd, resultado )
                    except:
                        print 'eval error:', tipoLeft, valorLeft, tipoRight, valorRight
                elif tipoLeft == 'n' and tipoRight in 'ifav':
                    if valorLeft not in aee.functions:     # variable on the left
                        if tipoRight != 'v':    # assign to variable
                            try:
                                aee.variables[ valorLeft ] = str( aee.evaluate( str( valorRight) ) )

                            except:
                                print 'exec error:', tipoLeft, valorLeft, tipoRight, valorRight
                                raise
                        else:                   # evaluate a variable
                            if valorLeft in aee.variables:
                                try:
                                    resultado = aee.variables[ valorLeft ]
                                    linea = writeResult( linea, mEqualSignAct.end(), RightActEnd, resultado )
                                except:
                                    print 'eval error:', tipoLeft, valorLeft, tipoRight, valorRight
                                    print linea
                                    raise
                    else:                                  # function on the left: evaluate
                        if valorLeft not in aee.functions[ valorLeft ]:
                            try:                # standard formula
                                resultado = str( aee.evaluate( valorLeft ) )
                                linea = writeResult( linea, mEqualSignAct.end(), RightActEnd, resultado )
                            except:
                                print 'eval error:', tipoLeft, valorLeft, tipoRight, valorRight
                        else:                   # recurrence relation
                            if valorLeft not in aee.variables:            # initial value
                                aee.variables[ valorLeft ] = str( aee.evaluate( str( valorRight ) ) )
                            else:                                         # iteration
                                resultado = str( aee.evaluate( aee.functions[ valorLeft ] ) )
                                linea = writeResult( linea, mEqualSignAct.end(), RightActEnd, resultado )
                                aee.variables[ valorLeft ] = resultado

                elif tipoLeft == 'n' and tipoRight in 'e': # define a function
                    try:
                        aee.functions[ valorLeft ] = str(valorRight)

                    except:
                        print 'exec error:', tipoLeft, valorLeft, tipoRight, valorRight
                        raise
                elif tipoLeft == 'n' and tipoRight in 'n': # define an alias
                    try:
                        aee.functions[ valorLeft ] = str(valorRight)

                    except:
                        print 'exec error:', tipoLeft, valorLeft, tipoRight, valorRight
                        raise



                RightPrevStart = mEqualSignAct.end()
                RightPrevEnd = RightActEnd

            if mEqualSignNext:
                mEqualSignNext = reEqualSign.search( linea, mEqualSignAct.end() )
            mEqualSignPrev = mEqualSignAct
            mEqualSignAct  = mEqualSignNext

        lines.append( linea )

    return '\n'.join( lines )


def writeResult( buffer, start, end, text ):
    'Return buffer with text applied from start to end offset.'

    return buffer[ :start ] + text + buffer[ end: ]


if __name__ == '__main__':
    import sys
    text = open( sys.argv[1] ).read()
    print feed( text )
