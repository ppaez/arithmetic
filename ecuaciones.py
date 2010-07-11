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
                        resultado = str( aee.evaluate( valorLeft ) )
                        line = writeResult( line, mEqualSignAct.end(), RightActEnd, resultado )
                    except:
                        print 'eval error:', tipoLeft, valorLeft, tipoRight, valorRight
                elif tipoLeft == 'n' and tipoRight == 'vNO' \
                        and valorLeft in aee.variables:    # evaluate variable or function
                    try: 
                        resultado = str( aee.evaluate( valorLeft ) )
                        line = writeResult( line, mEqualSignAct.end(), RightActEnd, resultado )
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
                                    line = writeResult( line, mEqualSignAct.end(), RightActEnd, resultado )
                                except:
                                    print 'eval error:', tipoLeft, valorLeft, tipoRight, valorRight
                                    print line
                                    raise
                    else:                                  # function on the left: evaluate
                        if valorLeft not in aee.functions[ valorLeft ]:
                            try:                # standard formula
                                resultado = str( aee.evaluate( valorLeft ) )
                                line = writeResult( line, mEqualSignAct.end(), RightActEnd, resultado )
                            except:
                                print 'eval error:', tipoLeft, valorLeft, tipoRight, valorRight
                        else:                   # recurrence relation
                            if valorLeft not in aee.variables:            # initial value
                                aee.variables[ valorLeft ] = str( aee.evaluate( str( valorRight ) ) )
                            else:                                         # iteration
                                resultado = str( aee.evaluate( aee.functions[ valorLeft ] ) )
                                line = writeResult( line, mEqualSignAct.end(), RightActEnd, resultado )
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
