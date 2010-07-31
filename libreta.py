#! /usr/bin/python

#   Copyright (c) 2010 Patricio Paez <pp@pp.com.mx>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>

import arithmetic


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
    texto.insert( Tkinter.END, arithmetic.feed( text ) )
    texto.mark_set( 'insert', cursorPosition )

def Quit( event ):
    'End the application.'
    root.quit()

# Build a simple editor window
import Tkinter
root = Tkinter.Tk()
texto = Tkinter.Text(root, height=40)
texto.pack()
texto.focus_set()

# Minimal configuration and key bindings
texto['font'] = ("lucida console", 11)
texto['wrap'] = Tkinter.NONE
texto.bind('<Control-l>', loadFile)
texto.bind('<Control-s>', saveFile)
texto.bind('<Control-q>', Quit)
texto.bind( '<F5>', Recalculate)

# Handle single parameter: filename
import sys
if len(sys.argv) > 1:
    filename = sys.argv[1]
    try:
        text = open( filename ).read()
        texto.insert( Tkinter.END, text )
    except:
        pass  # new file
else:
    filename = 'unnamed'
root.title( filename + ' - Libreta 0.2' )


root.mainloop()
