import ecuaciones


def openfile( event):
    text = open( sys.argv[1] ).read()
    texto.delete( '1.0', Tkinter.END )
    texto.insert( "1.0", text)


def KeyHandler( event ):
    if event.char=='\t':
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
texto.bind('<Control-o>', openfile)
texto.bind( '<Key>', KeyHandler)
texto.focus_set()	

import sys
text = open( sys.argv[1] ).read()
' Segundo parametro indica marcar cambios.'
if len(sys.argv) > 2:
    ecuaciones.marcarCambios = True


texto.insert( Tkinter.END, text )


root.mainloop()
