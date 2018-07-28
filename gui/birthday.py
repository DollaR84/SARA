"""
Graphic form add birthday.

Created on 26.06.2017

@author: Ruslan Dolovanyuk

"""

from gui.command import Command

import wx
import wx.adv


class AddBirthday(wx.Frame):
    """Created window for adding birthday."""

    def __init__(self, title, content, gui_phrases):
        """Initialize window adding birthday."""
        super().__init__(None, wx.ID_ANY, title, size=(800, 600))
        self.command = Command(self)
        self.birthday = content

        panel = wx.Panel(self, wx.ID_ANY)
        sizer_panel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panel.Add(panel, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer_panel)

        box_firstname = wx.StaticBox(panel, wx.ID_ANY, gui_phrases.firstname)
        box_lastname = wx.StaticBox(panel, wx.ID_ANY, gui_phrases.lastname)
        box_date = wx.StaticBox(panel, wx.ID_ANY, gui_phrases.date)
        box_category = wx.StaticBox(panel, wx.ID_ANY, gui_phrases.category)
        self.firstname = wx.TextCtrl(box_firstname, wx.ID_ANY)
        self.lastname = wx.TextCtrl(box_lastname, wx.ID_ANY)
        self.date = wx.adv.DatePickerCtrl(box_date, wx.ID_ANY,
                                          wx.DateTime.Today(),
                                          style=wx.adv.DP_DEFAULT)
        self.category = wx.ListBox(box_category, wx.ID_ANY,
                                   choices=self.birthday['category'],
                                   style=wx.LB_SINGLE | wx.LB_HSCROLL)
        self.category.SetSelection(self.birthday['index'])
        but_add = wx.Button(panel, wx.ID_ANY, gui_phrases.add)
        but_cancel = wx.Button(panel, wx.ID_ANY, gui_phrases.cancel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_firstname = wx.StaticBoxSizer(box_firstname, wx.VERTICAL)
        sizer_firstname.Add(self.firstname, 0, wx.EXPAND | wx.ALL, 5)
        sizer_lastname = wx.StaticBoxSizer(box_lastname, wx.VERTICAL)
        sizer_lastname.Add(self.lastname, 0, wx.EXPAND | wx.ALL, 5)
        sizer_date = wx.StaticBoxSizer(box_date, wx.VERTICAL)
        sizer_date.Add(self.date, 0, wx.EXPAND | wx.ALL, 5)
        sizer_category = wx.StaticBoxSizer(box_category, wx.VERTICAL)
        sizer_category.Add(self.category, 1, wx.EXPAND | wx.ALL, 5)
        sizer_buttons = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        sizer_buttons.Add(but_add, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        sizer_buttons.Add(but_cancel, 0,
                          wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(sizer_firstname, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer_lastname, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer_date, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer_category, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer_buttons, 0, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, getattr(self.command, 'close_window'))
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'close'), but_cancel)
        self.Bind(wx.EVT_BUTTON,
                  getattr(self.command, 'add_birthday'), but_add)

    def save(self, firstname, lastname, date, index):
        """Save result adding birthday information."""
        self.birthday['firstname'] = firstname
        self.birthday['lastname'] = lastname
        self.birthday['date'] = date
        self.birthday['index'] = index
