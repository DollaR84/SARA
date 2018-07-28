"""
The brain module of Sara.

Created on 26.11.2016

@author: Ruslan Dolovanyuk

"""

import logging
import os
import time

from assist import Assistant

from backups import Backups

import configs

from databases import Databases

from hotkeys import Hotkeys

from recognizer import Recognizer

from reference import Help

from speech import Speech


class Brain:
    """The brain class of Sara."""

    def __init__(self):
        """Initialize brain class of Sara."""
        self.log = logging.getLogger()
        self.log.info('initialize brain...')

        self.config = configs.default()
        if os.path.exists('user.json'):
            self.config = configs.update(self.config, 'user.json')

        self.speech = Speech(self.config.speech)

        self.speech.speak("Load language: " +
                          self.config.language.name[self.config.language.code])
        self.phrases = configs.language(self.config.language.languages_dir,
                                        self.config.language.code)
        self.help = Help(self.config.language, self.phrases)
        self.speech.speak(self.phrases.general.start)

        self.generals = {'quit': False, 'text': '', 'arg': None}

        self.bd = Databases(self.config.sqlite)
        self.assist = Assistant(self.speech, self.config,
                                self.phrases, self.bd)
        if True if "true" == self.config.general.setup else False:
            self.assist.setup()

        self.backups = Backups(self.config.backups, self.bd)
        self.hotkeys = Hotkeys(self.config.hotkeys, self.generals)
        self.recognizer = Recognizer(self.config.recognition,
                                     self.config.language.code,
                                     self.generals, self.speech,
                                     self.phrases.recognition)

    def mainloop(self):
        """Run main loop method."""
        self.log.info('run brain mainloop...')

        while True:

            self.recognizer.recognize()

            if self.generals['quit']:
                break

            self.check(self.generals['text'])
            self.assist.check(self.generals['text'], self.generals['arg'])
            self.generals['text'] = ''
            self.generals['arg'] = None
            time.sleep(0.1)

        self.quit()

    def quit(self):
        """Quit method from Sara."""
        self.log.info('quit Sara...')

        self.speech.speak(self.phrases.general.finish)
        self.bd.disconnect()
        self.hotkeys.clear()
        self.recognizer.finish()

    def reset(self):
        """Reset assistant brain of Sara."""
        self.log.info('reset assistant...')

        self.speech.speak(self.phrases.general.reset)
        self.assist.reset()

    def check(self, text):
        """Check need actions for use."""
        if 'help' == text:
            self.help.show_help()
        elif 'help_browser' == text:
            self.help.show_browser()
        elif 'features' == text:
            self.help.show_features()
        elif 'backup_bd' == text:
            self.speech.speak(self.phrases.backup.bd)
            self.backups.backup_bd()
        elif 'backup_user_data' == text:
            self.speech.speak(self.phrases.backup.user_data)
            self.backups.backup_user_data()
        elif 'backup_all' == text:
            self.speech.speak(self.phrases.backup.all)
            self.backups.backup_all()
        elif 'restore_bd' == text:
            self.speech.speak(self.phrases.restore.bd)
            self.backups.restore_bd()
            self.reset()
        elif 'restore_user_data' == text:
            self.speech.speak(self.phrases.restore.user_data)
            self.backups.restore_user_data()
        elif 'restore_all' == text:
            self.speech.speak(self.phrases.restore.all)
            self.backups.restore_all()
            self.reset()
