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
'''

igual = re.compile( '=' )
sigigual  = re.compile( '[^=]*=' )
sigsepar  = re.compile( '.*?  ' )
antigual= re.compile( '=[^=]*' )
antsepar = re.compile( '  .*' )
antdospuntos = re.compile( ':[^:]*' )

#print text
for linenumber, linea in enumerate( text.splitlines() ):
    salida = ''
    findelinea = linea
    long = len( linea )
    igualendant = 0
    igualstartant = 0
    derechastartanterior = 0
    derechaendanterior = 0
    m = igual.search( linea, igualendant )
    while m and igualendant < long:
        igualstart = m.start()
        igualend = m.end()
        if linea[ igualstart-1: igualstart ] != '=' and \
              linea[ igualend : igualend+1 ] != '=':
            # the smaller of msigigual, msigsepar, endofline
            derechaends = []
            msigigual = sigigual.search( linea, igualend )
            if msigigual:
                derechaends.append( msigigual.end() - 1 )
            msigsepar = sigsepar.search( linea, igualend )
            if msigsepar:
                derechaends.append( msigsepar.end() )
            derechaends.append( len( linea ) )
            derechaend = min( derechaends )
            #print derechaends
            # the larger of mantigual, mantsepar, mantdospuntos, beginofline
            izquierdastarts = []
            mantigual = antigual.search( linea, igualstartant, igualstart )
            if mantigual:
                #print mantigual.group(), mantigual.start(), mantigual.end()
                izquierdastarts.append( mantigual.start() + 1 )
            mantsepar = antsepar.search( linea, igualendant, igualstart )
            if mantsepar:
                #print mantsepar.group(), mantsepar.start(), mantsepar.end()
                izquierdastarts.append( mantsepar.start() + 2 )
            mantdospuntos = antdospuntos.search( linea, igualendant, igualstart )
            if mantdospuntos:
                izquierdastarts.append( mantdospuntos.start() + 2 )
            izquierdastarts.append( 0 )
            izquierdastart = max( izquierdastarts )
            #print izquierdastarts
            #print izquierdastart, derechaend,
            rangoizquierda = linea[ izquierdastart : igualstart ]
            rangocentro = linea[ igualstart : igualend ]
            rangoderecha = linea[ igualend : derechaend ] 
            if rangoizquierda.strip(): # i hay algo en la izquierda
                # analiza( rangoizquierda, rangoderecha )
                if not salida:
                    salida = '%2s %s' % ( linenumber, linea[ : izquierdastart ] ) 
                # no repetir lado izquierdo
                if derechastartanterior != izquierdastart or derechaendanterior != igualstart:
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
                derechastartanterior = igualend
                derechaendanterior = derechaend
                findelinea =  linea[ derechaend : ]
        igualstartant = igualstart
        igualendant = igualend
        m = igual.search( linea, igualendant )
    if salida:
        print salida + findelinea
    elif findelinea or igualendant == 0: 
        print '%2s %s' % ( linenumber, findelinea )
