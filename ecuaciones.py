import re, aee

reIgual = re.compile( ' ?= ?' )
reSepar = re.compile( '  +' )
reDospuntosLeft = re.compile( ': ' )

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

        RightAntStart = 0
        RightAntEnd = 0
        mIgualAnt = re.search( '^', linea )
        mIgualAct = reIgual.search( linea, mIgualAnt.end() )
        while mIgualAct:

            # Determine LeftActStart,
            # the larger of mIgualAnt, mSeparLeft, mDospuntosLeft, beginofline
            LeftStarts = []
            LeftStarts.append( mIgualAnt.end() )
            mSeparLeft = reSepar.search( linea, mIgualAnt.end(), mIgualAct.start() )
            if mSeparLeft:
                LeftStarts.append( mSeparLeft.end() )
            mDospuntosLeft = reDospuntosLeft.search( linea, mIgualAnt.end(), mIgualAct.start() )
            if mDospuntosLeft:
                LeftStarts.append( mDospuntosLeft.end() )
            mBeginOfLine = re.search( '^ *', linea )
            LeftStarts.append( mBeginOfLine.end() )
            LeftActStart = max( LeftStarts )

            # Determine RightActEnd,
            # the smaller of mIgualSig, mSeparDer, endofline
            RightEnds = []
            mIgualSig = reIgual.search( linea, mIgualAct.end() )
            if mIgualSig:
                RightEnds.append( mIgualSig.start() )
            mSeparDer = reSepar.search( linea, mIgualAct.end() )
            if mSeparDer:
                RightEnds.append( mSeparDer.start() )
            mEndOfLine = re.search( ' *$', linea )
            RightEnds.append( mEndOfLine.start() )
            RightActEnd = min( RightEnds )

            rangolibre     = linea[ RightAntEnd     : LeftActStart ]
            rangoLeft = linea[ LeftActStart : mIgualAct.start() ]
            rangocentro    = linea[ mIgualAct.start() : mIgualAct.end() ]
            rangoRight   = linea[ mIgualAct.end()   : RightActEnd ]

            tipoLeft, valorLeft = TypeAndValueOf( rangoLeft )
            tipoDer, valorDer = TypeAndValueOf( rangoRight )

            if tipoLeft != 'v': # there is something to the left

                # perform operations

                if tipoLeft in 'ea' and tipoDer in 'vif':  # evaluate expression
                    try:
                        resultado = str( aee.evaluate( valorLeft ) )
                        linea = writeResult( linea, mIgualAct.end(), RightActEnd, resultado )
                    except:
                        print 'eval error:', tipoLeft, valorLeft, tipoDer, valorDer
                elif tipoLeft == 'n' and tipoDer == 'vNO' \
                        and valorLeft in aee.variables:    # evaluate variable or function
                    try: 
                        resultado = str( aee.evaluate( valorLeft ) )
                        linea = writeResult( linea, mIgualAct.end(), RightActEnd, resultado )
                    except:
                        print 'eval error:', tipoLeft, valorLeft, tipoDer, valorDer
                elif tipoLeft == 'n' and tipoDer in 'ifav':
                    if valorLeft not in aee.functions:     # variable on the left
                        if tipoDer != 'v':      # assign to variable
                            try:
                                aee.variables[ valorLeft ] = str( aee.evaluate( str( valorDer) ) )

                            except:
                                print 'exec error:', tipoLeft, valorLeft, tipoDer, valorDer
                                raise
                        else:                   # evaluate a variable
                            if valorLeft in aee.variables:
                                try:
                                    resultado = aee.variables[ valorLeft ]
                                    linea = writeResult( linea, mIgualAct.end(), RightActEnd, resultado )
                                except:
                                    print 'eval error:', tipoLeft, valorLeft, tipoDer, valorDer
                                    print linea
                                    raise
                    else:                                  # function on the left: evaluate
                        if valorLeft not in aee.functions[ valorLeft ]:
                            try:                # standard formula
                                resultado = str( aee.evaluate( valorLeft ) )
                                linea = writeResult( linea, mIgualAct.end(), RightActEnd, resultado )
                            except:
                                print 'eval error:', tipoLeft, valorLeft, tipoDer, valorDer
                        else:                   # recurrence relation
                            if valorLeft not in aee.variables:            # initial value
                                aee.variables[ valorLeft ] = str( aee.evaluate( str( valorDer ) ) )
                            else:                                         # iteration
                                resultado = str( aee.evaluate( aee.functions[ valorLeft ] ) )
                                linea = writeResult( linea, mIgualAct.end(), RightActEnd, resultado )
                                aee.variables[ valorLeft ] = resultado

                elif tipoLeft == 'n' and tipoDer in 'e':   # define a function
                    try:
                        aee.functions[ valorLeft ] = str(valorDer)

                    except:
                        print 'exec error:', tipoLeft, valorLeft, tipoDer, valorDer
                        raise
                elif tipoLeft == 'n' and tipoDer in 'n':   # define an alias
                    try:
                        aee.functions[ valorLeft ] = str(valorDer)

                    except:
                        print 'exec error:', tipoLeft, valorLeft, tipoDer, valorDer
                        raise



                RightAntStart = mIgualAct.end()
                RightAntEnd = RightActEnd

            if mIgualSig:
                mIgualSig = reIgual.search( linea, mIgualAct.end() )
            mIgualAnt = mIgualAct
            mIgualAct = mIgualSig

        lines.append( linea )

    return '\n'.join( lines )


def writeResult( buffer, start, end, text ):
    'Return buffer with text applied from start to end offset.'

    return buffer[ :start ] + text + buffer[ end: ]


if __name__ == '__main__':
    import sys
    text = open( sys.argv[1] ).read()
    print feed( text )
