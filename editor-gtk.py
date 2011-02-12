
import gtk
import arithmetic

class Editor(object):
    'A minimal editor'

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file('editor.ui')
        self.builder.connect_signals(self)
        self.textview = self.builder.get_object( 'textview1' )


    def run(self):
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass
    
    def quit(self):
        gtk.main_quit()


    def on_window1_delete_event(self, *args):
        self.quit()

    def on_window1_button_press_event(self, *args):
        self.do_arithmetic()

    def do_arithmetic(self):
        'Perform arithmetic operations'

        # get the buffer
        buf = self.textview.get_buffer()

        # get cursor position as offset
        insert_iter = buf.get_iter_at_mark( buf.get_insert() )
        offset = insert_iter.get_offset()

        # parse and modify the text
        parser = arithmetic.ParserGTK()
        txt = parser.parse( buf )

        # set cursor position to previous offset
        insert_iter = buf.get_iter_at_offset( offset )
        buf.place_cursor( insert_iter )

if __name__ == '__main__':
        editor = Editor()
        editor.run()
