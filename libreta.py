import ecuaciones


def loadFile( event):
    'Load file content into the buffer.'
    text = open( sys.argv[1] ).read()
    texto.delete( '1.0', Tkinter.END )
    texto.insert( "1.0", text)

def saveFile( event):
    'Save the text buffer contents.'
    text = open( sys.argv[1] ), 'w' )
    text.write( texto.get( '1.0', Tkinter.END  ) )

def Recalculate( event ):
    '''Find arithmetic expressions and evalute them.

    Read text buffer, calculate, update the text buffer.'''

    text = texto.get( '1.0', Tkinter.END )
    texto.delete( '1.0', Tkinter.END )
    texto.insert( Tkinter.END, ecuaciones.feed( text ) )
    return "break"

import Tkinter
root = Tkinter.Tk()
texto = Tkinter.Text(root, height=40)
texto.pack()
texto['font'] = ("lucida console", 11)
texto['wrap'] = Tkinter.NONE
texto.bind('<Control-l>', loadFile)
texto.bind('<Control-s>', saveFile)
texto.bind( '<F5>', Recalculate)
texto.focus_set()	

import sys
text = open( sys.argv[1] ).read()
' Segundo parametro indica marcar cambios.'
if len(sys.argv) > 2:
    ecuaciones.marcarCambios = True


texto.insert( Tkinter.END, text )


root.mainloop()
