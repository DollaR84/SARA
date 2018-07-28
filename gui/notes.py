"""
Graphic form add note.

Created on 17.06.2017

@author: Ruslan Dolovanyuk

"""

from gui.command import Command

import wx


class AddNote(wx.Frame):
    """Created window for adding note."""

    def __init__(self, title, content, gui_phrases):
        """Initialize window adding note."""
        super().__init__(None, wx.ID_ANY, title, size=(800, 600))
        self.command = Command(self)
        self.note = content

        panel = wx.Panel(self, wx.ID_ANY)
        sizer_panel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panel.Add(panel, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer_panel)

        box_title = wx.StaticBox(panel, wx.ID_ANY, gui_phrases.title)
        box_data = wx.StaticBox(panel, wx.ID_ANY, gui_phrases.data)
        self.title = wx.TextCtrl(box_title, wx.ID_ANY)
        self.data = wx.TextCtrl(box_data, wx.ID_ANY,
                                style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        but_add = wx.Button(panel, wx.ID_ANY, gui_phrases.add)
        but_cancel = wx.Button(panel, wx.ID_ANY, gui_phrases.cancel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_title = wx.StaticBoxSizer(box_title, wx.VERTICAL)
        sizer_title.Add(self.title, 0, wx.EXPAND | wx.ALL, 5)
        sizer_data = wx.StaticBoxSizer(box_data, wx.VERTICAL)
        sizer_data.Add(self.data, 1, wx.EXPAND | wx.ALL, 5)
        sizer_buttons = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        sizer_buttons.Add(but_add, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        sizer_buttons.Add(but_cancel, 0,
                          wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(sizer_title, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer_data, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer_buttons, 0, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, getattr(self.command, 'close_window'))
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'close'), but_cancel)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'add_note'), but_add)

    def save(self, title, data):
        """Save result adding note information."""
        self.note['title'] = title
        self.note['data'] = data
