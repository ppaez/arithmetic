import re

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
                    expresion_python = re.sub( '([a-zA-Z][a-zA-Z0-9]*)', r'\1()', expresion_python )
                    return 'e', expresion_python
            return 'n', unaexpresion.replace( ' ', '' )

def feed( text ):
    'Feed text to the parser.  It is processed line by line.'

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

                if tipoIzq == 'e' and tipoDer == 'v':    # evalua expresion
                    try:
                        resultado = str( eval( valorIzq, globales ) )
                        linea = escribe( linea, mIgualAct.end(), DerechaActEnd, resultado, rangoderecha )
                    except:
                        print 'eval error:', tipoIzq, valorIzq, tipoDer, valorDer
                elif tipoIzq == 'n' and tipoDer == 'v' \
                        and valorIzq in globales.keys(): # evalua variable o funcion
                    try: 
                        resultado = str( eval( valorIzq + '()', globales ) )
                        linea = escribe( linea, mIgualAct.end(), DerechaActEnd, resultado, rangoderecha )
                    except:
                        print 'eval error:', tipoIzq, valorIzq, tipoDer, valorDer
                elif tipoIzq == 'n' and tipoDer in 'if':
                  if valorIzq not in funciones:          # asigna a variable
                    try:
                        exec valorIzq + ' = lambda : ' + str(valorDer) in globales

                    except:
                        print 'exec error:', tipoIzq, valorIzq, tipoDer, valorDer
                        raise
                  else:                                  # evalua funcion
                    try:
                        resultado = str( eval( valorIzq + '()', globales ) )
                        linea = escribe( linea, mIgualAct.end(), DerechaActEnd, resultado, rangoderecha )
                    except:
                        print 'eval error:', tipoIzq, valorIzq, tipoDer, valorDer
                elif tipoIzq == 'n' and tipoDer in 'e':  # define variable o funcion
                    try:
                        exec valorIzq + ' = lambda : ' + str(valorDer) in globales
                        if '()' in valorDer and valorIzq not in funciones:
                            funciones.append( valorIzq )

                    except:
                        print 'exec error:', tipoIzq, valorIzq, tipoDer, valorDer
                        raise
                elif tipoIzq == 'n' and tipoDer in 'n':  # define alias
                    try:
                        exec valorIzq + ' = lambda : ' + str(valorDer) in globales
                        if '()' in valorDer and valorIzq not in funciones:
                            funciones.append( valorIzq )

                    except:
                        print 'exec error:', tipoIzq, valorIzq, tipoDer, valorDer
                        raise



                DerechaAntStart = mIgualAct.end()
                DerechaAntEnd = DerechaActEnd

            mIgualAnt = mIgualAct
            mIgualAct = mIgualSig

        lines.append( linea )

    return '\n'.join( lines )


def escribe( buffer, inicio, final, texto, referencia ):
    'Regresa buffer con texto aplicado de inicio a final.'

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
