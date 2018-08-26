"""
Graphic form change settings.

Created on 17.08.2017

@author: Ruslan Dolovanyuk

"""

import os

from gui.command import Command

import wx


class Settings(wx.Frame):
    """Created window for change settings."""

    def __init__(self, title, content, gui_phrases):
        """Initialize window settings."""
        super().__init__(None, wx.ID_ANY, title, size=(800, 600))
        self.command = Command(self)
        self.content = content

        panel = wx.Panel(self, wx.ID_ANY)
        sizer_panel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panel.Add(panel, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer_panel)

        notebook = wx.Notebook(panel, wx.ID_ANY)
        self.general = TabGeneral(notebook, self.command,
                                  self.content, gui_phrases)
        self.language = TabLanguage(notebook, self.command,
                                    self.content, gui_phrases)
        self.speech = TabSpeech(notebook, self.command,
                                self.content, gui_phrases)
        self.recognition = TabRecognition(notebook, self.command,
                                          self.content, gui_phrases)
        self.database = TabDatabase(notebook, self.command,
                                    self.content, gui_phrases)
        self.backups = TabBackups(notebook, self.command,
                                  self.content, gui_phrases)
        self.hotkeys = TabHotkeys(notebook, self.command,
                                  self.content, gui_phrases)
        self.calendar = TabCalendar(notebook, self.command,
                                    self.content, gui_phrases)
        self.open = TabOpen(notebook, self.command,
                            self.content, gui_phrases)
        self.weather = TabWeather(notebook, self.command,
                                  self.content, gui_phrases)
        self.rss = TabRss(notebook, self.command,
                          self.content, gui_phrases)
        self.notes = TabNotes(notebook, self.command,
                              self.content, gui_phrases)
        self.birthday = TabBirthday(notebook, self.command,
                                    self.content, gui_phrases)
        self.events = TabEvents(notebook, self.command,
                                self.content, gui_phrases)
        notebook.AddPage(self.general, gui_phrases.general)
        notebook.AddPage(self.language, gui_phrases.language)
        notebook.AddPage(self.speech, gui_phrases.speech)
        notebook.AddPage(self.recognition, gui_phrases.recognition)
        notebook.AddPage(self.database, gui_phrases.database)
        notebook.AddPage(self.backups, gui_phrases.backups)
        notebook.AddPage(self.hotkeys, gui_phrases.hotkeys)
        notebook.AddPage(self.calendar, gui_phrases.calendar)
        notebook.AddPage(self.open, gui_phrases.open)
        notebook.AddPage(self.weather, gui_phrases.weather)
        notebook.AddPage(self.rss, gui_phrases.rss)
        notebook.AddPage(self.notes, gui_phrases.notes)
        notebook.AddPage(self.birthday, gui_phrases.birthday)
        notebook.AddPage(self.events, gui_phrases.events)

        but_save = wx.Button(panel, wx.ID_ANY, gui_phrases.save)
        but_cancel = wx.Button(panel, wx.ID_ANY, gui_phrases.cancel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_buttons = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        sizer_buttons.Add(but_save, 0,
                          wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        sizer_buttons.Add(but_cancel, 0,
                          wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer_buttons, 0, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, getattr(self.command, 'close_window'))
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'close'), but_cancel)
        self.Bind(wx.EVT_BUTTON,
                  getattr(self.command, 'save_settings'), but_save)


class TabGeneral(wx.Panel):
    """Page notebook for general settings."""

    def __init__(self, parent, command, content, gui_phrases):
        """Initialize page for general settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = content['config'].general

        version_str = gui_phrases.version % self.config.version
        version = wx.StaticText(self, wx.ID_ANY, version_str,
                                style=wx.EXPAND | wx.ALIGN_CENTER)
        box_user = wx.StaticBox(self, wx.ID_ANY, gui_phrases.box_user)
        self.user = wx.TextCtrl(box_user, wx.ID_ANY, self.config.user)

        sizer = wx.BoxSizer(wx.VERTICAL)
        user_sizer = wx.StaticBoxSizer(box_user, wx.HORIZONTAL)
        user_sizer.Add(self.user, 1, wx.ALL, 5)
        sizer.Add(version, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(user_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)


class TabLanguage(wx.Panel):
    """Page notebook for language settings."""

    def __init__(self, parent, command, content, gui_phrases):
        """Initialize page for language settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = content['config'].language
        self.codes = [code for code in self.config.name.keys()]
        self.names = [self.config.name[code] for code in self.codes]

        choice_language = wx.StaticText(self, wx.ID_ANY,
                                        gui_phrases.choice_language,
                                        style=wx.EXPAND | wx.ALIGN_LEFT)
        self.languages = wx.Choice(self, wx.ID_ANY, choices=self.names)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(choice_language, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.languages, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_CHOICE, getattr(command, 'choice_language'))

        self.languages.SetSelection(self.codes.index(self.config.code))


class TabSpeech(wx.Panel):
    """Page notebook for speech settings."""

    def __init__(self, parent, command, content, gui_phrases):
        """Initialize page for speech settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = content['config'].speech
        self.speech = content['speech']

        self.nvda = wx.CheckBox(self, wx.ID_ANY, gui_phrases.use_nvda)
        choice_voice = wx.StaticText(self, wx.ID_ANY, gui_phrases.choice_voice,
                                     style=wx.EXPAND | wx.ALIGN_LEFT)
        self.voices = wx.Choice(self, wx.ID_ANY,
                                choices=self.speech.voices_names)
        box_rate = wx.StaticBox(self, wx.ID_ANY, gui_phrases.rate_voice)
        self.rate_slider = wx.Slider(box_rate, wx.ID_ANY,
                                     self.config.rate, -10, 10,
                                     style=wx.SL_HORIZONTAL |
                                     wx.SL_AUTOTICKS |
                                     wx.SL_LABELS)
        self.rate_slider.SetTickFreq(5)
        box_volume = wx.StaticBox(self, wx.ID_ANY, gui_phrases.volume_voice)
        self.volume_slider = wx.Slider(box_volume, wx.ID_ANY,
                                       self.config.volume, 0, 100,
                                       style=wx.SL_HORIZONTAL |
                                       wx.SL_AUTOTICKS |
                                       wx.SL_LABELS)
        self.volume_slider.SetTickFreq(10)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.nvda, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(choice_voice, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.voices, 0, wx.EXPAND | wx.ALL, 5)
        sizer_rate = wx.StaticBoxSizer(box_rate, wx.VERTICAL)
        sizer_rate.Add(self.rate_slider, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer_rate, 0, wx.EXPAND | wx.ALL, 5)
        sizer_volume = wx.StaticBoxSizer(box_volume, wx.VERTICAL)
        sizer_volume.Add(self.volume_slider, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer_volume, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_CHECKBOX, getattr(command, 'use_nvda'), self.nvda)
        self.Bind(wx.EVT_CHOICE, getattr(command, 'choice_voice'))
        self.Bind(wx.EVT_SLIDER,
                  getattr(command, 'slider_rate'), self.rate_slider)
        self.Bind(wx.EVT_SLIDER,
                  getattr(command, 'slider_volume'), self.volume_slider)

        self.voices.SetSelection(self.config.voice)
        nvda = True if self.config.nvda == "true" else False
        self.nvda.SetValue(nvda)
        if nvda:
            self.voices.Disable()
            self.rate_slider.Disable()
            self.volume_slider.Disable()


class TabRecognition(wx.Panel):
    """Page notebook for recognition settings."""

    def __init__(self, parent, command, content, gui_phrases):
        """Initialize page for recognition settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = content['config'].recognition

        empty = wx.StaticText(self, wx.ID_ANY, gui_phrases.empty,
                              style=wx.EXPAND | wx.ALIGN_CENTER)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(empty, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)


class TabDatabase(wx.Panel):
    """Page notebook for database settings."""

    def __init__(self, parent, command, content, gui_phrases):
        """Initialize page for database settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = content['config'].sqlite

        empty = wx.StaticText(self, wx.ID_ANY, gui_phrases.empty,
                              style=wx.EXPAND | wx.ALIGN_CENTER)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(empty, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)


class TabBackups(wx.Panel):
    """Page notebook for backups settings."""

    def __init__(self, parent, command, content, gui_phrases):
        """Initialize page for backups settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = content['config'].backups
        self.path = ''

        tar_list = wx.StaticText(self, wx.ID_ANY, gui_phrases.tar_list,
                                 style=wx.EXPAND | wx.ALIGN_LEFT)
        self.listbox = wx.ListBox(self, wx.ID_ANY, choices=[],
                                  style=wx.LB_SINGLE | wx.LB_HSCROLL)
        self.but_delete = wx.Button(self, wx.ID_ANY, gui_phrases.delete)
        box_add = wx.StaticBox(self, wx.ID_ANY, gui_phrases.box_add)
        box_name = wx.StaticBox(box_add, wx.ID_ANY, gui_phrases.box_name)
        self.name = wx.TextCtrl(box_name, wx.ID_ANY, '')
        box_path = wx.StaticBox(box_add, wx.ID_ANY, gui_phrases.box_path)
        self.path_browse = wx.DirPickerCtrl(box_path, wx.ID_ANY,
                                            '', gui_phrases.browse_dir)
        but_add = wx.Button(box_add, wx.ID_ANY, gui_phrases.add)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tar_list, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.but_delete, 0, wx.ALIGN_LEFT, 5)
        add_sizer = wx.StaticBoxSizer(box_add, wx.VERTICAL)
        name_sizer = wx.StaticBoxSizer(box_name, wx.HORIZONTAL)
        name_sizer.Add(self.name, 1, wx.EXPAND | wx.ALL, 5)
        add_sizer.Add(name_sizer, 0, wx.EXPAND | wx.ALL, 5)
        path_sizer = wx.StaticBoxSizer(box_path, wx.HORIZONTAL)
        path_sizer.Add(self.path_browse, 1, wx.EXPAND | wx.ALL, 5)
        add_sizer.Add(path_sizer, 0, wx.EXPAND | wx.ALL, 5)
        add_sizer.Add(but_add, 0, wx.ALIGN_LEFT, 5)
        sizer.Add(add_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_LISTBOX, getattr(command, 'tar_selection'))
        self.Bind(wx.EVT_BUTTON,
                  getattr(command, 'tar_delete'), self.but_delete)
        self.Bind(wx.EVT_DIRPICKER_CHANGED, getattr(command, 'tar_browse'))
        self.Bind(wx.EVT_BUTTON, getattr(command, 'tar_add'), but_add)

        self.set_tar_names()
        self.path_browse.GetPickerCtrl().SetLabel(gui_phrases.browse)
        self.but_delete.Disable()

    def set_tar_names(self):
        """Generate names for tar list user data."""
        self.tar_list = [name for name in self.config.user_data.keys()]
        self.tar_names = [name + ' (' + self.config.user_data[name] + ')'
                          for name in self.tar_list]
        self.listbox.Set(self.tar_names)
        self.Layout()


class TabHotkeys(wx.Panel):
    """Page notebook for hotkeys settings."""

    def __init__(self, parent, command, content, gui_phrases):
        """Initialize page for hotkeys settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = content['config'].hotkeys

        empty = wx.StaticText(self, wx.ID_ANY, gui_phrases.empty,
                              style=wx.EXPAND | wx.ALIGN_CENTER)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(empty, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)


class TabCalendar(wx.Panel):
    """Page notebook for calendar settings."""

    def __init__(self, parent, command, content, gui_phrases):
        """Initialize page for calendar settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = content['config'].calendar
        self.formats = ['24', '12']

        choice_time_format = wx.StaticText(self, wx.ID_ANY,
                                           gui_phrases.choice_time_format,
                                           style=wx.EXPAND | wx.ALIGN_LEFT)
        self.time_formats = wx.Choice(self, wx.ID_ANY, choices=self.formats)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(choice_time_format, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.time_formats, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_CHOICE, getattr(command, 'choice_time_format'))

        index = self.formats.index(str(self.config.time_format))
        self.time_formats.SetSelection(index)


class TabOpen(wx.Panel):
    """Page notebook for open settings."""

    def __init__(self, parent, command, content, gui_phrases):
        """Initialize page for open settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = content['config'].presser

        empty = wx.StaticText(self, wx.ID_ANY, gui_phrases.empty,
                              style=wx.EXPAND | wx.ALIGN_CENTER)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(empty, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)


class TabWeather(wx.Panel):
    """Page notebook for weather settings."""

    def __init__(self, parent, command, content, gui_phrases):
        """Initialize page for weather settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = content['config'].weather

        self.metric = wx.CheckBox(self, wx.ID_ANY, gui_phrases.metric)
        box_country = wx.StaticBox(self, wx.ID_ANY, gui_phrases.box_country)
        self.country = wx.TextCtrl(box_country, wx.ID_ANY, self.config.country)
        box_city = wx.StaticBox(self, wx.ID_ANY, gui_phrases.box_city)
        self.city = wx.TextCtrl(box_city, wx.ID_ANY, self.config.city)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.metric, 0, wx.EXPAND | wx.ALL, 5)
        country_sizer = wx.StaticBoxSizer(box_country, wx.HORIZONTAL)
        country_sizer.Add(self.country, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(country_sizer, 0, wx.EXPAND | wx.ALL, 5)
        city_sizer = wx.StaticBoxSizer(box_city, wx.HORIZONTAL)
        city_sizer.Add(self.city, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(city_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

        if "true" == self.config.metric:
            self.metric.SetValue(True)
        else:
            self.metric.SetValue(False)


class TabRss(wx.Panel):
    """Page notebook for rss settings."""

    def __init__(self, parent, command, content, gui_phrases):
        """Initialize page for rss settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = content['config'].rss

        feed_list = wx.StaticText(self, wx.ID_ANY, gui_phrases.feed_list,
                                  style=wx.EXPAND | wx.ALIGN_LEFT)
        self.listbox = wx.ListBox(self, wx.ID_ANY, choices=[],
                                  style=wx.LB_SINGLE | wx.LB_HSCROLL)
        self.but_delete = wx.Button(self, wx.ID_ANY, gui_phrases.delete)
        box_add = wx.StaticBox(self, wx.ID_ANY, gui_phrases.box_add)
        box_name = wx.StaticBox(box_add, wx.ID_ANY, gui_phrases.box_name)
        self.name = wx.TextCtrl(box_name, wx.ID_ANY, '')
        box_url = wx.StaticBox(box_add, wx.ID_ANY, gui_phrases.box_url)
        self.url = wx.TextCtrl(box_url, wx.ID_ANY, '')
        but_add = wx.Button(box_add, wx.ID_ANY, gui_phrases.add)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(feed_list, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.but_delete, 0, wx.ALIGN_LEFT, 5)
        add_sizer = wx.StaticBoxSizer(box_add, wx.VERTICAL)
        name_sizer = wx.StaticBoxSizer(box_name, wx.HORIZONTAL)
        name_sizer.Add(self.name, 1, wx.EXPAND | wx.ALL, 5)
        add_sizer.Add(name_sizer, 0, wx.EXPAND | wx.ALL, 5)
        url_sizer = wx.StaticBoxSizer(box_url, wx.HORIZONTAL)
        url_sizer.Add(self.url, 1, wx.EXPAND | wx.ALL, 5)
        add_sizer.Add(url_sizer, 0, wx.EXPAND | wx.ALL, 5)
        add_sizer.Add(but_add, 0, wx.ALIGN_LEFT, 5)
        sizer.Add(add_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_LISTBOX, getattr(command, 'feed_selection'))
        self.Bind(wx.EVT_BUTTON,
                  getattr(command, 'feed_delete'), self.but_delete)
        self.Bind(wx.EVT_BUTTON, getattr(command, 'feed_add'), but_add)

        self.set_names()
        self.but_delete.Disable()

    def set_names(self):
        """Generate names list for feeds."""
        self.names = [feed[0] for feed in self.config.feeds]
        self.listbox.Set(self.names)
        self.Layout()


class TabNotes(wx.Panel):
    """Page notebook for notes settings."""

    def __init__(self, parent, command, content, gui_phrases):
        """Initialize page for notes settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = content['config'].notes

        empty = wx.StaticText(self, wx.ID_ANY, gui_phrases.empty,
                              style=wx.EXPAND | wx.ALIGN_CENTER)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(empty, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)


class TabBirthday(wx.Panel):
    """Page notebook for birthday settings."""

    def __init__(self, parent, command, content, gui_phrases):
        """Initialize page for birthday settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = content['config'].birthday
        self.update_file = os.path.join(self.config.file_path,
                                        self.config.file_name)
        wildcard = 'Update file (*.update)|*.update'

        box_update_file = wx.StaticBox(self, wx.ID_ANY,
                                       gui_phrases.box_update_file)
        self.update_file_browse = wx.FilePickerCtrl(box_update_file, wx.ID_ANY,
                                                    self.update_file,
                                                    gui_phrases.browse_file,
                                                    wildcard)

        sizer = wx.BoxSizer(wx.VERTICAL)
        update_file_sizer = wx.StaticBoxSizer(box_update_file, wx.HORIZONTAL)
        update_file_sizer.Add(self.update_file_browse, 1,
                              wx.EXPAND | wx.ALL, 5)
        sizer.Add(update_file_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_FILEPICKER_CHANGED,
                  getattr(command, 'birthday_browse'))

        self.update_file_browse.GetPickerCtrl().SetLabel(gui_phrases.browse)


class TabEvents(wx.Panel):
    """Page notebook for events settings."""

    def __init__(self, parent, command, content, gui_phrases):
        """Initialize page for events settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = content['config'].events
        self.update_file = os.path.join(self.config.file_path,
                                        self.config.file_name)
        wildcard = 'Update file (*.update)|*.update'

        box_update_file = wx.StaticBox(self, wx.ID_ANY,
                                       gui_phrases.box_update_file)
        self.update_file_browse = wx.FilePickerCtrl(box_update_file, wx.ID_ANY,
                                                    self.update_file,
                                                    gui_phrases.browse_file,
                                                    wildcard)

        sizer = wx.BoxSizer(wx.VERTICAL)
        update_file_sizer = wx.StaticBoxSizer(box_update_file, wx.HORIZONTAL)
        update_file_sizer.Add(self.update_file_browse, 1,
                              wx.EXPAND | wx.ALL, 5)
        sizer.Add(update_file_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_FILEPICKER_CHANGED, getattr(command, 'events_browse'))

        self.update_file_browse.GetPickerCtrl().SetLabel(gui_phrases.browse)
