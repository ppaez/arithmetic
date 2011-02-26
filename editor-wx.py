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

def calculate(event):
    if event.GetKeyCode() == wx.WXK_F5:
        control = event.GetEventObject()
        nlines = control.GetNumberOfLines()
        lines = []
        for i in range(nlines):
            lines.append( control.GetLineText(i) )
        text = '\n'.join( lines )
        parser = Parser()
        text = parser.parse(text)
        end = control.GetLastPosition()
        control.Replace( 0, end, text )
    event.Skip()

app = wx.App(False)
frame = Editor(None, 'wxWidgets editor')
app.MainLoop()
