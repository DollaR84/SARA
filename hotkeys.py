"""
Watch global hotkeys.

Created on 15.01.2017

@author: Ruslan Dolovanyuk

"""

import logging

import keyboard


class Hotkeys:
    """Class watch globals hotkeys."""

    def __init__(self, config, generals):
        """Initialize class Hotkeys."""
        self.log = logging.getLogger()
        self.log.info('initialize hotkeys...')

        self.config = config
        self.generals = generals

        for key, value in self.config.__dict__.items():
            keyboard.add_hotkey(value, self.check, (key,))

    def clear(self):
        """Clear all hotkeys from system."""
        self.log.info('clear all hotkeys...')

        keyboard.clear_all_hotkeys()

    def check(self, key):
        """Check hotkey was pressed."""
        self.log.info('catch hotkey %s: %s' % (key, self.config.__dict__[key]))

        if 'quit' == key:
            self.generals[key] = True
        else:
            self.generals['text'] = key
