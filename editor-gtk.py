#! /usr/bin/env python

import sys
import os
import gtk
from arithmetic import Parser

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


class ParserGTK(Parser):
    ''

    def parse( self, textBuffer ):
        ''
        for i in range( self.countLines( textBuffer ) ):
            self.parseLine( i, textBuffer, variables=self.variables, functions=self.functions )

    def countLines( self, textBuffer ):
        ''
        return textBuffer.get_line_count()

    def readLine( self, i, textBuffer ):
        ''
        iter_start = textBuffer.get_iter_at_line( i )
        if iter_start.ends_line():
            return ''
        else:
            iter_end = textBuffer.get_iter_at_line( i )
            iter_end.forward_to_line_end()
            return textBuffer.get_text( iter_start, iter_end )

    def writeResult( self, i, textBuffer, start, end, text ):
        'Write text in line i of lines from start to end offset.'
        # Delete
        if end > start:
            # handle start at end of line or beyond
            iter_line = textBuffer.get_iter_at_line( i )
            nchars = iter_line.get_chars_in_line()
            if start > nchars-1:
                start = nchars-1
            iter_start = textBuffer.get_iter_at_line_offset( i, start )
            iter_end = textBuffer.get_iter_at_line_offset( i, end )
            textBuffer.delete( iter_start, iter_end )

        # Insert
        iter_start = textBuffer.get_iter_at_line_offset( i, start )
        textBuffer.insert( iter_start, text )


def calculate( widget, event, textbuffer ):
    'Perform arithmetic operations'

    if event.keyval == gtk.keysyms.F5:
        parser = ParserGTK()
        parser.parse( textbuffer )

if __name__ == '__main__':
        editor = Editor()
        editor.run()
