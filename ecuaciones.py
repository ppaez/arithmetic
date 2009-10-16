import re

text = '''
=====
= = = = =
Supongamos: base = 5 x 3 =   para empezar.
  altura= 2   radio=   lado = 5
base x altura =

perimetro = (base + altura) x 2 =
 perimetro =

   Calculo de pension de cesantia:

semanas cotizadas = sc = 1,350
salario promedio = 1,200
cuantia basica = salario promedio x 0.13
cuantia basica =    es el resultado final.
             a = 3                       
             3 =
'''

reIgual = re.compile( ' ?= ?' )
reSepar = re.compile( '  +' )
reDospuntosIzq = re.compile( ': ' )

def TipoValorDe( unaexpresion ):
    "Regresa tipo 'i', 'f', 'e', 'o' y valor."

    if not unaexpresion.strip():  # vacio
        return 'v', '0'
    try:
        n = int( unaexpresion.replace( ',', '' ) )
        return 'i', n
    except:
        try:
            n = float( unaexpresion.replace( ',', '' ) )
            return 'f', n
        except:
            expresion_asterisco = re.sub( r'\bx\b', '*', unaexpresion )
            for op in '+-*/':
                if op in expresion_asterisco:
                    expresion = op
                    return 'e', expresion_asterisco
            return 'n', unaexpresion.replace( ' ', '' )


for linenumber, linea in enumerate( text.splitlines() ):
    salida = ''
    findelinea = linea
    DerechaAntStart = 0
    DerechaAntEnd = 0
    mIgualAnt = re.search( '^', linea )
    mIgualAct = reIgual.search( linea, mIgualAnt.end() )
    while mIgualAct:

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

        rangoizquierda = linea[ izquierdaActStart : mIgualAct.start() ]
        rangocentro = linea[ mIgualAct.start() : mIgualAct.end() ]
        rangoderecha = linea[ mIgualAct.end() : DerechaActEnd ] 

        if rangoizquierda.strip(): # si hay algo en la izquierda
            # analiza( rangoizquierda, rangoderecha )
            if not salida:
                salida = '%2s ' % ( linenumber )
            salida = salida + '%s' % ( linea[ DerechaAntEnd : izquierdaActStart ] )

            tipoIzq, valorIzq = TipoValorDe( rangoizquierda )
            tipoDer, valorDer = TipoValorDe( rangoderecha )
            if tipoIzq == 'e' and tipoDer == 'v':
                try:
                    rangoderecha = eval( valorIzq )
                except:
                    pass

            # no repetir lado izquierdo
            if DerechaAntStart != izquierdaActStart or DerechaAntEnd != mIgualAct.start():
                if tipoIzq in 'ifv':
                    salida = salida + '[%s]' % ( rangoizquierda ) 
                elif tipoIzq == 'e':
                    salida = salida + '{%s}' % ( rangoizquierda )
                else:
                    salida = salida + '<%s>' % ( rangoizquierda )
            # = y el lado derecho
            if tipoDer in 'ifv':
                salida = salida + '%s[%s]' % ( rangocentro, 
                                    rangoderecha )
            elif tipoDer == 'e':
                salida = salida + '%s{%s}' % ( rangocentro, 
                                    rangoderecha )
            else:
                salida = salida + '%s<%s>' % ( rangocentro, 
                                    rangoderecha )
            DerechaAntStart = mIgualAct.end()
            DerechaAntEnd = DerechaActEnd
            findelinea =  linea[ DerechaActEnd : ]

        mIgualAnt = mIgualAct
        mIgualAct = mIgualSig
    if salida:
        print salida + findelinea
    elif findelinea or mIgualAnt.end() == 0: 
        print '%2s %s' % ( linenumber, findelinea )
