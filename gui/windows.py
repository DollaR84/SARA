"""
Graphic form windows.

Created on 14.06.2017

@author: Ruslan Dolovanyuk

"""

from gui.command import Command

import wx
import wx.html


class AppWindow:
    """Simple class for running graphical form."""

    def __init__(self, window, gui_phrases):
        """Initialize simple app."""
        self.wnd = window
        self.gui_phrases = gui_phrases
        self.app = wx.App()

    def run(self, title, content):
        """Run window form."""
        window = self.wnd(title, content, self.gui_phrases)
        window.Show(True)
        self.app.SetTopWindow(window)
        self.app.MainLoop()


class HtmlWindow(wx.Frame):
    """Created html window."""

    def __init__(self, title, content, gui_phrases):
        """Initialize html window."""
        super().__init__(None, wx.ID_ANY, title, size=(800, 600))
        self.command = Command(self)

        panel = wx.Panel(self, wx.ID_ANY)
        sizer_panel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panel.Add(panel, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer_panel)

        html = wx.html.HtmlWindow(panel)
        html.SetPage(content)
        button = wx.Button(panel, wx.ID_ANY, gui_phrases.close)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER, 5)
        panel.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, getattr(self.command, 'close_window'))
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'close'), button)


class TextWindow(wx.Frame):
    """Created text window."""

    def __init__(self, title, content, gui_phrases):
        """Initialize text window."""
        super().__init__(None, wx.ID_ANY, title, size=(800, 600))
        self.command = Command(self)

        panel = wx.Panel(self, wx.ID_ANY)
        sizer_panel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panel.Add(panel, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer_panel)

        text = wx.TextCtrl(panel, wx.ID_ANY,
                           style=wx.TE_MULTILINE | wx.TE_READONLY)
        text.SetValue(content)
        button = wx.Button(panel, wx.ID_ANY, gui_phrases.close)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER, 5)
        panel.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, getattr(self.command, 'close_window'))
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'close'), button)
