"""
Help module of Sara.

Created on 10.02.2017

@author: Ruslan Dolovanyuk

"""

import logging
import os

from gui.windows import AppWindow
from gui.windows import HtmlWindow
from gui.windows import TextWindow


class Help:
    """Class help for Sara."""

    def __init__(self, config, phrases):
        """Initialize help class."""
        self.log = logging.getLogger()
        self.log.info('initialize help...')

        self.config = config
        self.phrases = phrases.reference
        self.gui_phrases = phrases.gui

    def get_html_path(self):
        """Return html path."""
        file_name = self.config.code + '.html'
        file_path = os.path.join(self.config.languages_dir,
                                 self.config.help_dir)
        html_file = os.path.join(file_path, file_name)
        return os.path.normpath(html_file)

    def show_help(self):
        """Show html help."""
        self.log.info('show help html file...')

        with open(self.get_html_path(), 'rb') as data:
            content = data.read()

            wnd = AppWindow(HtmlWindow, self.gui_phrases)
            wnd.run(self.phrases.title_help, content.decode('utf-8'))

    def show_browser(self):
        """Show html help in browser."""
        self.log.info('show help html file in browser...')

        os.startfile(self.get_html_path())

    def show_features(self):
        """Show features information."""
        self.log.info('show features information')

        wnd = AppWindow(TextWindow, self.gui_phrases)
        wnd.run(self.phrases.title_features, self.get_features())

    def get_features(self):
        """Get features information."""
        self.log.info('Get features from file...')

        file_name = self.config.code + '.txt'
        file_path = os.path.join(self.config.languages_dir,
                                 self.config.features_dir)
        features_path = os.path.join(file_path, file_name)

        with open(features_path, 'rb') as data:
            features = data.read()
            return features.decode('utf-8')
