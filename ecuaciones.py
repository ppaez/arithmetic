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

semanas cotizadas = 1,350
salario promedio = 1,200
cuantia basica = salario promedio x 0.13
cuantia basica =    es el resultado final.
             a = 3                       
'''

reIgual = re.compile( ' ?= ?' )

reSeparSig  = re.compile( '  +' )
reIgualAnt = re.compile( ' ?= ?' )
reSeparIzq = re.compile( '  +' )
reDospuntosIzq = re.compile( ': ' )

#print text
for linenumber, linea in enumerate( text.splitlines() ):
    salida = ''
    findelinea = linea
    long = len( linea )
    IgualAntEnd = 0
    IgualAntStart = 0
    IgualSigStart = 0
    IgualSigEnd = 0
    DerechaAntStart = 0
    DerechaAntEnd = 0
    mIgual = reIgual.search( linea, IgualAntEnd )
    if mIgual:
        IgualActStart = mIgual.start()
        IgualActEnd = mIgual.end()
    while mIgual:
        if True:
        #if linea[ IgualActStart-1: IgualActStart ] != '=' and \
        #      linea[ IgualActEnd : IgualActEnd+1 ] != '=':

            # the larger of mIgualAnt, mSeparIzq, mDospuntosIzq, beginofline
            IzquierdaStarts = []
            mIgualAnt = reIgualAnt.search( linea, IgualAntStart, IgualActStart )
            if mIgualAnt:
                IzquierdaStarts.append( mIgualAnt.end() )
            mSeparIzq = reSeparIzq.search( linea, IgualAntEnd, IgualActStart )
            if mSeparIzq:
                IzquierdaStarts.append( mSeparIzq.end() )
            mDospuntosIzq = reDospuntosIzq.search( linea, IgualAntEnd, IgualActStart )
            if mDospuntosIzq:
                IzquierdaStarts.append( mDospuntosIzq.end() )
            mBeginOfLine = re.search( '^ *', linea )
            IzquierdaStarts.append( mBeginOfLine.end() )
            izquierdaActStart = max( IzquierdaStarts )

            # the smaller of mIgualSig, mSeparDer, endofline
            DerechaEnds = []
            mIgualSig = reIgual.search( linea, IgualActEnd )
            if mIgualSig:
                IgualSigStart = mIgualSig.start()
                IgualSigEnd = mIgualSig.end()
                DerechaEnds.append( mIgualSig.start() )
            else:
                IgualSigStart = 0
                IgualSigEnd = 0
            mSeparDer = reSeparSig.search( linea, IgualActEnd )
            if mSeparDer:
                DerechaEnds.append( mSeparDer.start() )
            mEndOfLine = re.search( ' *$', linea )
            DerechaEnds.append( mEndOfLine.start() )
            DerechaActEnd = min( DerechaEnds )

            rangoizquierda = linea[ izquierdaActStart : IgualActStart ]
            rangocentro = linea[ IgualActStart : IgualActEnd ]
            rangoderecha = linea[ IgualActEnd : DerechaActEnd ] 

            if rangoizquierda.strip(): # si hay algo en la izquierda
                # analiza( rangoizquierda, rangoderecha )
                if not salida:
                    salida = '%2s ' % ( linenumber )
                salida = salida + '%s' % ( linea[ DerechaAntEnd : izquierdaActStart ] )
                # no repetir lado izquierdo
                if DerechaAntStart != izquierdaActStart or DerechaAntEnd != IgualActStart:
                    salida = salida + '<%s>' % ( rangoizquierda )
                # = y el lado derecho
                n = ''; expresion = ''
                try:
                    n = int( rangoderecha.replace( ',', '' ) )
                except:
                    try:
                        n = float( rangoderecha.replace( ',', '' ) )
                    except:
                        expresion_asterisco = re.sub( r'\bx\b', '*', rangoderecha )
                        for op in '+-*/':
                            if op in expresion_asterisco:
                                expresion = op
                                break
                if not rangoderecha.strip():  # vacio
                    n = '0'
                if n:
                    salida = salida + '%s[%s]' % ( rangocentro, 
                                        rangoderecha )
                elif expresion:
                    salida = salida + '%s{%s}' % ( rangocentro, 
                                        rangoderecha )
                else:
                    salida = salida + '%s<%s>' % ( rangocentro, 
                                        rangoderecha )
                DerechaAntStart = IgualActEnd
                DerechaAntEnd = DerechaActEnd
                findelinea =  linea[ DerechaActEnd : ]

        IgualAntStart = IgualActStart
        IgualAntEnd = IgualActEnd
        IgualActStart = IgualSigStart
        IgualActEnd = IgualSigEnd
        mIgual = mIgualSig
    if salida:
        print salida + findelinea
    elif findelinea or IgualAntEnd == 0: 
        print '%2s %s' % ( linenumber, findelinea )
