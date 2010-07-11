#! /usr/bin/python

import ecuaciones


def loadFile( event):
    'Load file content into the buffer.'

    cursorPosition = texto.index( 'insert' )
    text = open( filename ).read()
    texto.delete( '1.0', Tkinter.END )
    texto.insert( "1.0", text)
    texto.mark_set( 'insert', cursorPosition )

def saveFile( event):
    'Save the text buffer contents.'
    text = open( filename, 'w' )
    text.write( texto.get( '1.0', Tkinter.END  ) )

def Recalculate( event ):
    '''Find arithmetic expressions and evalute them.

    Read text buffer, calculate, update the text buffer.'''

    cursorPosition = texto.index( 'insert' )
    text = texto.get( '1.0', Tkinter.END )
    texto.delete( '1.0', Tkinter.END )
    texto.insert( Tkinter.END, ecuaciones.feed( text ) )
    texto.mark_set( 'insert', cursorPosition )

def Quit( event ):
    'End the application.'
    root.quit()

# Build a simple editor window
import Tkinter
root = Tkinter.Tk()
texto = Tkinter.Text(root, height=40)
texto.pack()
texto['font'] = ("lucida console", 11)
texto['wrap'] = Tkinter.NONE
texto.bind('<Control-l>', loadFile)
texto.bind('<Control-s>', saveFile)
texto.bind('<Control-q>', Quit)
texto.bind( '<F5>', Recalculate)
texto.focus_set()	

import sys
if len(sys.argv) > 1:
    filename = sys.argv[1]
    try:
        text = open( filename ).read()
        texto.insert( Tkinter.END, text )
    except:
        pass  # new file

root.mainloop()
