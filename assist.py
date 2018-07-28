"""
The assistant for brain of Sara.

Created on 19.01.2017

@author: Ruslan Dolovanyuk

"""

import logging
import os
import time

import configs

from extensions import birthday
from extensions import calendar
from extensions import events
from extensions import notes
from extensions import presser
from extensions import rss
from extensions import weather


class Pointer:
    """Class pointer on resources for extensions."""

    def __init__(self, speech, phrases, bd, func_notice):
        """Initialize class for save pointers."""
        self.speech = speech
        self.phrases = phrases
        self.bd = bd
        self.notice = func_notice

        self.rss_start = 1
        self.rss_next = False
        self.rss_source = None


class Assistant:
    """The assistant class for brain of Sara."""

    def __init__(self, speech, config, phrases, bd):
        """Initialize assistant class for brain Sara."""
        self.log = logging.getLogger()
        self.log.info('initialize assistant...')

        self.speech = speech
        self.config = config
        self.phrases = phrases
        self.bd = bd

        self.ptr = Pointer(self.speech, self.phrases, self.bd, self.notice)
        self.reset()
        if "true" == self.config.general.setup:
            configs.open_settings(self.ptr, self.config)

    def reset(self):
        """First run and reset assistant."""
        self.hello()

        if birthday.if_exists(self.ptr, self.config.birthday):
            birthday.notice(self.ptr)
        else:
            birthday.setup(self.ptr, self.config.birthday)

        if events.if_exists(self.ptr, self.config.events):
            events.notice(self.ptr)
        else:
            events.setup(self.ptr, self.config.events)

        if not notes.if_exists(self.ptr, self.config.notes):
            notes.setup(self.ptr, self.config.notes)

        if not rss.if_exists(self.ptr, self.config.rss):
            rss.setup(self.ptr, self.config.rss)

        if not weather.if_exists(self.ptr, self.config.weather):
            weather.setup(self.ptr, self.config.weather)

    def check(self, text, arg):
        """Check need actions for use."""
        if 'hello' == text:
            self.hello()
        elif 'settings' == text:
            configs.open_settings(self.ptr, self.config)
        elif 'version' == text:
            self.speech.speak(
              self.phrases.general.version + str(self.config.general.version))

        calendar.check(self.ptr, self.config.calendar, text)
        presser.check(self.ptr, self.config.presser, text)
        birthday.check(self.ptr, self.config.birthday, text, arg)
        events.check(self.ptr, self.config.events, text, arg)
        notes.check(self.ptr, self.config.notes, text, arg)
        rss.check(self.ptr, self.config.rss, text, arg)
        weather.check(self.ptr, self.config.weather, text,
                      arg, self.config.language.code)

    def hello(self):
        """Say hello method."""
        self.log.info('say hello...')

        hour = int(time.strftime('%H', time.localtime()))
        if 6 <= hour < 12:
            self.speech.speak(
              self.phrases.hello.morning % self.config.general.user)
        elif 12 <= hour < 18:
            self.speech.speak(
              self.phrases.hello.day % self.config.general.user)
        elif 18 <= hour < 24:
            self.speech.speak(
              self.phrases.hello.evening % self.config.general.user)
        else:
            self.speech.speak(
              self.phrases.hello.night % self.config.general.user)

    def notice(self):
        """Play sound and say notes."""
        self.log.info('out notice...')

        sound = os.path.join(
          self.config.general.sounds_dir, self.config.general.notice)
        self.speech.play(sound)
        self.speech.speak(self.phrases.general.notice)

    def setup(self):
        """Run setup methods in extensions."""
        birthday.setup(self.ptr, self.config.birthday)
        events.setup(self.ptr, self.config.events)
        notes.setup(self.ptr, self.config.notes)
        rss.setup(self.ptr, self.config.rss)
        weather.setup(self.ptr, self.config.weather)
