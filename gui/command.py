"""
Commands for gui forms.

Created on 17.06.2017

@author: Ruslan Dolovanyuk

"""

import os


class Command:
    """Commands for windows form in sara project."""

    def __init__(self, window):
        """Initialize command class."""
        self.wnd = window

    def add_birthday(self, event):
        """Adding birthday in database."""
        self.wnd.save(self.wnd.firstname.GetValue(),
                      self.wnd.lastname.GetValue(),
                      self.wnd.date.GetValue().Format('%d.%m.%Y'),
                      self.wnd.category.GetSelection())
        self.wnd.Close(True)

    def add_event(self, event):
        """Adding event in database."""
        self.wnd.save(self.wnd.date.GetValue().Format('%d.%m.%Y'),
                      self.wnd.data.GetValue())
        self.wnd.Close(True)

    def add_note(self, event):
        """Adding note in database."""
        self.wnd.save(self.wnd.title.GetValue(), self.wnd.data.GetValue())
        self.wnd.Close(True)

    def use_nvda(self, event):
        """Change value checkbox use nvda."""
        page = self.wnd.speech
        if page.nvda.GetValue():
            page.voices.Disable()
            page.rate_slider.Disable()
            page.volume_slider.Disable()
        else:
            page.voices.Enable()
            page.rate_slider.Enable()
            page.volume_slider.Enable()

    def choice_voice(self, event):
        """Change voice in SAPI."""
        page = self.wnd.speech
        page.speech.set_voice(page.voices.GetSelection())

    def slider_rate(self, event):
        """Change rate voice in SAPI."""
        page = self.wnd.speech
        page.speech.set_rate(page.rate_slider.GetValue())

    def slider_volume(self, event):
        """Change volume voice in SAPI."""
        page = self.wnd.speech
        page.speech.set_volume(page.volume_slider.GetValue())

    def save_settings(self, event):
        """Save settings."""
        page = self.wnd.general
        page.config.user = page.user.GetValue()
        page = self.wnd.speech
        page.config.nvda = "true" if page.nvda.IsChecked() else "false"
        page.config.voice = page.voices.GetSelection()
        page.config.rate = page.rate_slider.GetValue()
        page.config.volume = page.volume_slider.GetValue()
        page = self.wnd.weather
        page.config.metric = "true" if page.metric.IsChecked() else "false"
        page.config.country = page.country.GetValue()
        page.config.city = page.city.GetValue()
        page = self.wnd.birthday
        update_file = os.path.split(page.update_file)
        page.config.file_path = update_file[0]
        page.config.file_name = update_file[1]
        page = self.wnd.events
        update_file = os.path.split(page.update_file)
        page.config.file_path = update_file[0]
        page.config.file_name = update_file[1]
        self.wnd.content['save'] = True
        self.wnd.Close(True)

    def close(self, event):
        """Close event for button close."""
        self.wnd.Close(True)

    def close_window(self, event):
        """Close window event."""
        self.wnd.Destroy()

    def choice_language(self, event):
        """Change language."""
        page = self.wnd.language
        page.config.code = page.codes[page.languages.GetSelection()]

    def choice_voice(self, event):
        """Change voice."""
        page = self.wnd.speech
        page.config.voice = page.voices.GetSelection()
        page.speech.set_voice(page.config.voice)

    def slider_rate(self, event):
        """Change select rate slider."""
        page = self.wnd.speech
        page.speech.set_rate(page.rate_slider.GetValue())

    def slider_volume(self, event):
        """Change select volume slider."""
        page = self.wnd.speech
        page.speech.set_volume(page.volume_slider.GetValue())

    def tar_selection(self, event):
        """Change selection user data backups."""
        page = self.wnd.backups
        page.but_delete.Enable()

    def tar_delete(self, event):
        """Delete row in user data backups."""
        page = self.wnd.backups
        index = page.listbox.GetSelection()
        page.config.user_data.pop(page.tar_list[index])
        page.set_tar_names()
        page.but_delete.Disable()

    def tar_browse(self, event):
        """Select path user dir for backups."""
        page = self.wnd.backups
        page.path = page.path_browse.GetPath()

    def tar_add(self, event):
        """Add row in user data backups."""
        page = self.wnd.backups
        name = page.name.GetValue()
        if ('' != name) and ('' != page.path):
            page.config.user_data[name] = page.path
            page.set_tar_names()

    def choice_time_format(self, event):
        """Choice time format for calendar."""
        page = self.wnd.calendar
        index = page.time_formats.GetSelection()
        page.config.time_format = int(page.formats[index])

    def feed_selection(self, event):
        """Change selection in feed list."""
        page = self.wnd.rss
        page.but_delete.Enable()

    def feed_delete(self, event):
        """Delete row in rss feed list."""
        page = self.wnd.rss
        index = page.listbox.GetSelection()
        page.config.feeds.pop(index)
        page.set_names()
        page.but_delete.Disable()

    def feed_add(self, event):
        """Add row in feed list."""
        page = self.wnd.rss
        name = page.name.GetValue()
        url = page.url.GetValue()
        if ('' != name) and ('' != url):
            page.config.feeds.append([name, url])
            page.set_names()

    def birthday_browse(self, event):
        """Select update file user data."""
        page = self.wnd.birthday
        page.update_file = page.update_file_browse.GetPath()

    def events_browse(self, event):
        """Select update file user data."""
        page = self.wnd.events
        page.update_file = page.update_file_browse.GetPath()
