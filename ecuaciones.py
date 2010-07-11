import re, aee

reIgual = re.compile( ' ?= ?' )
reSepar = re.compile( '  +' )
reDospuntosIzq = re.compile( ': ' )

globales = { '__builtins__' : '' }
funciones = []


def TipoValorDe( unaexpresion ):
    "Regresa tipo 'i', 'f', 'e', 'o' y valor."

    if not unaexpresion.strip():  # vacio
        return 'v', ''
    try:
        n = int( unaexpresion.replace( ',', '' ) )
        return 'i', n
    except:
        try:
            n = float( unaexpresion.replace( ',', '' ) )
            return 'f', n
        except:
            expresion_python = re.sub( r'\bx\b', '*', unaexpresion )
            expresion_python = re.sub( r'%', '/100.', expresion_python )
            for op in '+-*/':
                if op in expresion_python:
                    expresion_python = expresion_python.replace( ' ', '' )
                    if re.search( '([a-zA-Z][a-zA-Z0-9]*)', expresion_python ):
                        return 'e', expresion_python  # expression with names
                    return 'a', expresion_python
            return 'n', unaexpresion.replace( ' ', '' )

def feed( text ):
    'Feed text to the parser.  It is processed line by line.'

    # Initialize
    aee.functions = {}
    aee.variables = {}

    lines = []

    for linenumber, linea in enumerate( text.splitlines() ):

        DerechaAntStart = 0
        DerechaAntEnd = 0
        mIgualAnt = re.search( '^', linea )
        mIgualAct = reIgual.search( linea, mIgualAnt.end() )
        while mIgualAct:

            # Determina izquierdaActStart
            # the larger of mIgualAnt, mSeparIzq, mDospuntosIzq, beginofline
            IzquierdaStarts = []
            IzquierdaStarts.append( mIgualAnt.end() )
            mSeparIzq = reSepar.search( linea, mIgualAnt.end(), mIgualAct.start() )
            if mSeparIzq:
                IzquierdaStarts.append( mSeparIzq.end() )
            mDospuntosIzq = reDospuntosIzq.search( linea, mIgualAnt.end(), mIgualAct.start() )
            if mDospuntosIzq:
                IzquierdaStarts.append( mDospuntosIzq.end() )
            mBeginOfLine = re.search( '^ *', linea )
            IzquierdaStarts.append( mBeginOfLine.end() )
            izquierdaActStart = max( IzquierdaStarts )

            # Determina DerechaActEnd
            # the smaller of mIgualSig, mSeparDer, endofline
            DerechaEnds = []
            mIgualSig = reIgual.search( linea, mIgualAct.end() )
            if mIgualSig:
                DerechaEnds.append( mIgualSig.start() )
            mSeparDer = reSepar.search( linea, mIgualAct.end() )
            if mSeparDer:
                DerechaEnds.append( mSeparDer.start() )
            mEndOfLine = re.search( ' *$', linea )
            DerechaEnds.append( mEndOfLine.start() )
            DerechaActEnd = min( DerechaEnds )

            rangolibre     = linea[ DerechaAntEnd     : izquierdaActStart ]
            rangoizquierda = linea[ izquierdaActStart : mIgualAct.start() ]
            rangocentro    = linea[ mIgualAct.start() : mIgualAct.end() ]
            rangoderecha   = linea[ mIgualAct.end()   : DerechaActEnd ] 

            tipoIzq, valorIzq = TipoValorDe( rangoizquierda )
            tipoDer, valorDer = TipoValorDe( rangoderecha )

            if tipoIzq != 'v': # si hay algo en la izquierda

                # hacer operaciones

                if tipoIzq in 'ea' and tipoDer in 'vif':    # evalua expresion
                    try:
                        resultado = str( aee.evaluate( valorIzq ) )
                        linea = escribe( linea, mIgualAct.end(), DerechaActEnd, resultado )
                    except:
                        print 'eval error:', tipoIzq, valorIzq, tipoDer, valorDer
                elif tipoIzq == 'n' and tipoDer == 'vNO' \
                        and valorIzq in aee.variables: # evalua variable o funcion
                    try: 
                        resultado = str( aee.evaluate( valorIzq ) )
                        linea = escribe( linea, mIgualAct.end(), DerechaActEnd, resultado )
                    except:
                        print 'eval error:', tipoIzq, valorIzq, tipoDer, valorDer
                elif tipoIzq == 'n' and tipoDer in 'ifav':
                    if valorIzq not in aee.functions:      # variable
                        if tipoDer != 'v':      # asigna a variable
                            try:
                                aee.variables[ valorIzq ] = str( aee.evaluate( str( valorDer) ) )

                            except:
                                print 'exec error:', tipoIzq, valorIzq, tipoDer, valorDer
                                raise
                        else:                   # evalua variable
                            if valorIzq in aee.variables:
                                try:
                                    resultado = aee.variables[ valorIzq ]
                                    linea = escribe( linea, mIgualAct.end(), DerechaActEnd, resultado )
                                except:
                                    print 'eval error:', tipoIzq, valorIzq, tipoDer, valorDer
                                    print linea
                                    raise
                    else:                       # evalua funcion
                        if valorIzq not in aee.functions[ valorIzq ]:
                            try:                     # standard formula
                                resultado = str( aee.evaluate( valorIzq ) )
                                linea = escribe( linea, mIgualAct.end(), DerechaActEnd, resultado )
                            except:
                                print 'eval error:', tipoIzq, valorIzq, tipoDer, valorDer
                        else:                        # recurrence relation
                            if valorIzq not in aee.variables:             # initial value
                                aee.variables[ valorIzq ] = str( aee.evaluate( str( valorDer ) ) )
                            else:                                         # iteration
                                resultado = str( aee.evaluate( aee.functions[ valorIzq ] ) )
                                linea = escribe( linea, mIgualAct.end(), DerechaActEnd, resultado )
                                aee.variables[ valorIzq ] = resultado

                elif tipoIzq == 'n' and tipoDer in 'e':  # define funcion
                    try:
                        aee.functions[ valorIzq ] = str(valorDer)

                    except:
                        print 'exec error:', tipoIzq, valorIzq, tipoDer, valorDer
                        raise
                elif tipoIzq == 'n' and tipoDer in 'n':  # define alias
                    try:
                        aee.functions[ valorIzq ] = str(valorDer)

                    except:
                        print 'exec error:', tipoIzq, valorIzq, tipoDer, valorDer
                        raise



                DerechaAntStart = mIgualAct.end()
                DerechaAntEnd = DerechaActEnd

            if mIgualSig:
                mIgualSig = reIgual.search( linea, mIgualAct.end() )
            mIgualAnt = mIgualAct
            mIgualAct = mIgualSig

        lines.append( linea )

    return '\n'.join( lines )


def escribe( buffer, inicio, final, texto ):
    'Regresa buffer con texto aplicado de inicio a final.'

    referencia = buffer[ inicio : final ]
    if texto == referencia or not marcarCambios:
        return buffer[ :inicio ] + texto + buffer[ final: ]
    else:
        return buffer[ :inicio ] + texto + '<-' + buffer[ final: ]

marcarCambios = False

if __name__ == '__main__':
    import sys
    text = open( sys.argv[1] ).read()
    ' Segundo parametro indica marcar cambios.'
    if len(sys.argv) > 2:
        marcarCambios = True
    print feed( text )
