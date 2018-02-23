#! /usr/bin/env python

import wx
from arithmetic import Parser

class Editor(wx.Frame):
    'A minimal editor.'

    def __init__(self, parent, title):
         wx.Frame.__init__(self, parent, title=title, size=(800,600))
         self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
         self.control.Bind( wx.EVT_KEY_DOWN, calculate)
         self.Show(True)


class ParserWx(Parser):
    ''

    def parse( self, TextControl ):
        ''
        for i in range( self.countLines( TextControl ) ):
            self.parseLine( i, TextControl, variables=self.variables, functions=self.functions )

    def countLines( self, TextControl ):
        ''
        return TextControl.GetNumberOfLines()

    def readLine( self, i, TextControl ):
        ''
        return TextControl.GetLineText(i)

    def writeResult( self, i, TextControl, start, end, text ):
        'Write text in line i of lines from start to end offset.'

        # Convert line, column to offset
        startOffset = TextControl.XYToPosition( start, i)
        endOffset = TextControl.XYToPosition( end, i)
        TextControl.Replace( startOffset, endOffset, text )


def calculate(event):
    'Perform arithmetic operations'

    if event.GetKeyCode() == wx.WXK_F5:
        textcontrol = event.GetEventObject()
        parser = ParserWx()
        parser.parse( textcontrol )
    event.Skip()

app = wx.App(False)
frame = Editor(None, 'wxWidgets editor')
app.MainLoop()
