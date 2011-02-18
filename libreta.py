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

    cursorPosition = event.widget.index( 'insert' )
    text = open( event.widget.filename ).read()
    event.widget.delete( '1.0', Tkinter.END )
    event.widget.insert( "1.0", text)
    event.widget.mark_set( 'insert', cursorPosition )

def saveFile( event):
    'Save the text buffer contents.'
    text = open( filename, 'w' )
    text.write( event.widget.get( '1.0', Tkinter.END  ) )

def Recalculate( event ):
    '''Find arithmetic expressions and evalute them.

    Read text buffer, calculate, update the text buffer.'''

    parser = arithmetic.ParserTk()
    parser.parse( event.widget )

def Quit( event ):
    'End the application.'
    root.quit()

# Build a simple editor window
import Tkinter

class Editor(object):
    'A minimal editor'

    def __init__(self, root):
        self.texto = Tkinter.Text(root, height=40)
        self.texto.pack()
        self.texto.focus_set()

        # Minimal configuration and key bindings
        self.texto['font'] = ("lucida console", 11)
        self.texto['wrap'] = Tkinter.NONE
        self.texto.bind('<Control-l>', loadFile)
        self.texto.bind('<Control-s>', saveFile)
        self.texto.bind('<Control-q>', Quit)
        self.texto.bind( '<F5>', Recalculate)

        # Handle single parameter: filename
        import sys
        if len(sys.argv) > 1:
            self.texto.filename = sys.argv[1]
            try:
                text = open( self.texto.filename ).read()
                self.texto.insert( Tkinter.END, text )
            except:
                pass  # new file
        else:
            self.texto.filename = 'unnamed'
        root.title( self.texto.filename + ' - Libreta 0.5' )


root = Tkinter.Tk()
editor = Editor(root)
root.mainloop()
