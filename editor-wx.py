#! /usr/bin/env python

import wx
from arithmetic import ParserWx

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
        parser = ParserWx()
        parser.parse( control )
    event.Skip()

app = wx.App(False)
frame = Editor(None, 'wxWidgets editor')
app.MainLoop()
