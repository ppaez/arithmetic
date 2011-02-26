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

import sys
import Tkinter
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
    text = open( event.widget.filename, 'w' )
    text.write( event.widget.get( '1.0', Tkinter.END  ) )


class Editor(object):
    'A minimal editor'

    def __init__(self):
        self.root = Tkinter.Tk()
        self.texto = Tkinter.Text(self.root, height=40)
        self.texto.pack()
        self.texto.focus_set()

        # Minimal configuration and key bindings
        self.texto['font'] = ("lucida console", 11)
        self.texto['wrap'] = Tkinter.NONE
        self.texto.bind('<Control-l>', loadFile)
        self.texto.bind('<Control-s>', saveFile)
        self.texto.bind('<Control-q>', self.quit)
        self.texto.bind( '<F5>', calculate)

        # Handle single parameter: filename
        if len(sys.argv) > 1:
            self.texto.filename = sys.argv[1]
            try:
                text = open( self.texto.filename ).read()
                self.texto.insert( Tkinter.END, text )
            except:
                pass  # new file
        else:
            self.texto.filename = 'unnamed'
        self.root.title( self.texto.filename + ' - editor-Tk' )

    def run(self):
        self.root.mainloop()

    def quit( self, event ):
        'End the application.'
        self.root.quit()

def calculate( event ):
    'Perform arithmetic operations'

    parser = arithmetic.ParserTk()
    parser.parse( event.widget )

editor = Editor()
editor.run()
