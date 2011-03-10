#! /usr/bin/env python

import sys
import os
import gtk
import arithmetic

class Editor(object):
    'A minimal editor'

    def __init__(self):
        # path to UI file
        scriptPath = os.path.split( sys.argv[0] )[0]
        uiFilePath = os.path.join( scriptPath,'editor.ui' )

        self.builder = gtk.Builder()
        self.builder.add_from_file( uiFilePath )
        self.builder.connect_signals(self)
        self.textview = self.builder.get_object( 'textview1' )
        self.buffer = self.textview.get_buffer()
        self.textview.connect( "key_press_event", calculate, self.buffer )
        if len( sys.argv ) > 1:
            text = open( sys.argv[1] ).read()
            self.buffer.set_text( text )


    def run(self):
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass
    
    def quit(self):
        gtk.main_quit()


    def on_window1_delete_event(self, *args):
        self.quit()

def calculate( widget, event, textbuffer ):
    'Perform arithmetic operations'

    if event.keyval == gtk.keysyms.F5:
        parser = arithmetic.ParserGTK()
        parser.parse( textbuffer )

if __name__ == '__main__':
        editor = Editor()
        editor.run()
