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



if __name__ == '__main__':
    'Test this module.'

    import sys

    if len( sys.argv ) == 1:
        'Test lexical analyzer only.'

        class doc:
            text =  '''5x3 123456 123,456 123.456  123456%
        1 10 1000 123,456,678.123 .1 .2 -1 *nombre_largo nombre doble + - x / * ** ^
        5 x xili x 5x3 + 5.x3 + 5x.3 * 5+x - a5x3 + a5 x 3 * a5x(3) / X x 3 - ( base x area ) ^ x3+x
        5x3
        sin( angle ) + offset'''
            offset = 0
        print doc.text
        print

        t = gettoken( doc )
        while t:
            print t,
            t = gettoken( doc )

    else:
        'Test evaluate()'

        variables[ 'a' ] = '100'
        variables[ 'f' ] = '10'
        functions[ 'f' ] = 'a x 5'

        import sys
        testexpression = sys.argv[ 1 ]
        print 
        print testexpression
        print evaluate( testexpression )
