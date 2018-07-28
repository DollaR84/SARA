"""
Graphic form add event.

Created on 26.06.2017

@author: Ruslan Dolovanyuk

"""

from gui.command import Command

import wx
import wx.adv


class AddEvent(wx.Frame):
    """Created window for adding event."""

    def __init__(self, title, content, gui_phrases):
        """Initialize window adding event."""
        super().__init__(None, wx.ID_ANY, title, size=(800, 600))
        self.command = Command(self)
        self.event = content

        panel = wx.Panel(self, wx.ID_ANY)
        sizer_panel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panel.Add(panel, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer_panel)

        box_date = wx.StaticBox(panel, wx.ID_ANY, gui_phrases.date)
        box_data = wx.StaticBox(panel, wx.ID_ANY, gui_phrases.data)
        self.date = wx.adv.DatePickerCtrl(box_date, wx.ID_ANY,
                                          wx.DateTime.Today(),
                                          style=wx.adv.DP_DEFAULT)
        self.data = wx.TextCtrl(box_data, wx.ID_ANY,
                                style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        but_add = wx.Button(panel, wx.ID_ANY, gui_phrases.add)
        but_cancel = wx.Button(panel, wx.ID_ANY, gui_phrases.cancel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_date = wx.StaticBoxSizer(box_date, wx.VERTICAL)
        sizer_date.Add(self.date, 0, wx.EXPAND | wx.ALL, 5)
        sizer_data = wx.StaticBoxSizer(box_data, wx.VERTICAL)
        sizer_data.Add(self.data, 1, wx.EXPAND | wx.ALL, 5)
        sizer_buttons = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        sizer_buttons.Add(but_add, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        sizer_buttons.Add(but_cancel, 0,
                          wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(sizer_date, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer_data, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer_buttons, 0, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, getattr(self.command, 'close_window'))
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'close'), but_cancel)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'add_event'), but_add)

    def save(self, date, data):
        """Save result adding event information."""
        self.event['date'] = date
        self.event['data'] = data
