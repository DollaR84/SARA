"""
The recognizer module.

Created on 26.11.2016

@author: Ruslan Dolovanyuk

"""

import logging
import os
import pickle

import configs

from pocketsphinx import LiveSpeech

import pyaudio

import recognizer2


class Recognizer:
    """The recognizer class."""

    def __init__(self, config, lang_code, generals, speech, phrases):
        """Initialize recognizer class."""
        self.log = logging.getLogger()
        self.log.info('initialize recognizer...')

        self.config = config
        self.generals = generals
        self.speech = speech
        self.phrases = phrases

        self.loader(lang_code)
        self.rss_source_flag = False

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=16000,
                                      input=True,
                                      frames_per_buffer=1024)
        self.stream.start_stream()

        self.in_speech_bf = False
        self.voice.set_search('keyphrase')
        self.voice.start_utt()

    def loader(self, lang_code):
        """Load language files for recognition."""
        self.log.info('load language files for recognition...')

        code_path = os.path.join(self.config.recognition_dir, lang_code)
        jsgf_path = os.path.join(code_path, self.config.jsgf_dir)
        variants_path = os.path.join(code_path, self.config.variants_dir)

        self.variants = {}
        self.keywords = configs.language_obj(code_path, self.config.keywords_name)

        hmm_path = os.path.join(code_path, self.config.hmm_name)
        dic_file = os.path.join(code_path, self.config.dic_name + '.dic')
        self.voice = LiveSpeech(hmm=hmm_path, lm=False, dic=dic_file)

        for name in self.config.jsgf_names:
            file_name = os.path.join(jsgf_path, name + '.jsgf')
            self.voice.set_jsgf_file(name, file_name)
            file_name = os.path.join(variants_path, name + '.dat')
            with open(file_name, 'rb') as variant:
                self.variants[name] = pickle.load(variant).split('\n')

    def finish(self):
        """Finish recognizing and close audio streams."""
        self.log.info('close audio streams...')

        self.voice.end_utt()
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def recognize(self):
        """Run main recognizing loop."""
        buffer = self.stream.read(1024)

        if buffer:
            self.voice.process_raw(buffer, False, False)

            if self.voice.get_in_speech() != self.in_speech_bf:
                self.in_speech_bf = self.voice.get_in_speech()

                if not self.in_speech_bf:
                    self.voice.end_utt()
                    self.check(self.voice.hypothesis())
                    self.voice.start_utt()

    def check(self, text):
        """Check voice phrases."""
        self.log.info('recognition: %s' % text)
        section = self.voice.get_search()

        if 'keyphrase' == section:
            if self.keywords.total.keyphrase == text:
                self.voice.set_search('main')
                self.play('enable')
        elif self.keywords.total.variants == text:
            self.speak_variants()
        elif self.keywords.total.cancel == text:
            self.cancel()
        elif 'main' == section:
            self.section_main(text)
        elif 'calendar' == section:
            self.section_calendar(text)
        elif 'rss' == section:
            self.section_rss(text)
        elif 'weather' == section:
            self.section_weather(text)
        elif 'open' == section:
            self.section_open(text)
        elif 'notes' == section:
            self.section_notes(text)
        elif 'birthday' == section:
            self.section_birthday(text)
        elif 'events' == section:
            self.section_events(text)
        elif 'backups' == section:
            self.section_backups(text)

    def section_main(self, text):
        """Check phrases from main section."""
        self.log.info('search main section')

        if self.keywords.main.hello == text:
            self.generals['text'] = 'hello'
            self.complete()
        elif self.keywords.main.version == text:
            self.generals['text'] = 'version'
            self.complete()
        elif ((self.keywords.main.help == text) or
              (self.keywords.main.help2 == text)):
            self.generals['text'] = 'help'
            self.complete()
            self.speech.speak(self.phrases.help)
        elif ((self.keywords.main.help_browser == text) or
              (self.keywords.main.help_browser2 == text)):
            self.generals['text'] = 'help_browser'
            self.complete()
            self.speech.speak(self.phrases.help_browser)
        elif self.keywords.main.features == text:
            self.generals['text'] = 'features'
            self.complete()
            self.speech.speak(self.phrases.features)
        elif self.keywords.main.calendar == text:
            self.play('disable')
            self.voice.set_search('calendar')
            self.speech.speak(self.phrases.calendar)
            self.play('enable')
        elif self.keywords.main.rss == text:
            self.play('disable')
            self.voice.set_search('rss')
            self.speech.speak(self.phrases.rss)
            self.generals['text'] = 'rss_source'
            self.play('enable')
        elif self.keywords.main.weather == text:
            self.play('disable')
            self.voice.set_search('weather')
            self.speech.speak(self.phrases.weather)
            self.play('enable')
        elif self.keywords.main.open == text:
            self.play('disable')
            self.voice.set_search('open')
            self.speech.speak(self.phrases.open)
            self.play('enable')
        elif self.keywords.main.notes == text:
            self.play('disable')
            self.voice.set_search('notes')
            self.speech.speak(self.phrases.notes)
            self.play('enable')
        elif self.keywords.main.birthday == text:
            self.play('disable')
            self.voice.set_search('birthday')
            self.speech.speak(self.phrases.birthday)
            self.play('enable')
        elif self.keywords.main.events == text:
            self.play('disable')
            self.voice.set_search('events')
            self.speech.speak(self.phrases.events)
            self.play('enable')
        elif self.keywords.main.backups == text:
            self.play('disable')
            self.voice.set_search('backups')
            self.speech.speak(self.phrases.backups)
            self.play('enable')
        elif self.keywords.main.settings == text:
            self.generals['text'] = 'settings'
            self.complete()
        elif ((self.keywords.main.exit == text) or
              (self.keywords.main.exit2 == text)):
            self.generals['quit'] = True
            self.complete()
        else:
            self.failure()

    def section_calendar(self, text):
        """Check phrases from calendar section."""
        self.log.info('search calendar section')

        if self.keywords.calendar.date_now == text:
            self.generals['text'] = 'date_now'
            self.elaboration()
        elif self.keywords.calendar.date_detail == text:
            self.generals['text'] = 'date_detail'
            self.elaboration()
        elif self.keywords.calendar.weekday == text:
            self.generals['text'] = 'weekday'
            self.elaboration()
        elif ((self.keywords.calendar.time_now == text) or
              (self.keywords.calendar.time_now2 == text) or
              (self.keywords.calendar.time_now3 == text)):
            self.generals['text'] = 'time_now'
            self.elaboration()
        else:
            self.failure()

    def section_weather(self, text):
        """Check phrases from weather section."""
        self.log.info('search weather section')

        if self.keywords.weather.today == text:
            self.generals['text'] = 'weather_today'
            self.elaboration()
        elif self.keywords.weather.today_day == text:
            self.generals['text'] = 'weather_today'
            self.generals['arg'] = 'day'
            self.elaboration()
        elif self.keywords.weather.today_night == text:
            self.generals['text'] = 'weather_today'
            self.generals['arg'] = 'night'
            self.elaboration()
        elif self.keywords.weather.tomorrow == text:
            self.generals['text'] = 'weather_tomorrow'
            self.elaboration()
        elif self.keywords.weather.tomorrow_day == text:
            self.generals['text'] = 'weather_tomorrow'
            self.generals['arg'] = 'day'
            self.elaboration()
        elif self.keywords.weather.tomorrow_night == text:
            self.generals['text'] = 'weather_tomorrow'
            self.generals['arg'] = 'night'
            self.elaboration()
        elif self.keywords.weather.monday == text:
            self.generals['text'] = 'weather_monday'
            self.elaboration()
        elif self.keywords.weather.monday_day == text:
            self.generals['text'] = 'weather_monday'
            self.generals['arg'] = 'day'
            self.elaboration()
        elif self.keywords.weather.monday_night == text:
            self.generals['text'] = 'weather_monday'
            self.generals['arg'] = 'night'
            self.elaboration()
        elif self.keywords.weather.tuesday == text:
            self.generals['text'] = 'weather_tuesday'
            self.elaboration()
        elif self.keywords.weather.tuesday_day == text:
            self.generals['text'] = 'weather_tuesday'
            self.generals['arg'] = 'day'
            self.elaboration()
        elif self.keywords.weather.tuesday_night == text:
            self.generals['text'] = 'weather_tuesday'
            self.generals['arg'] = 'night'
            self.elaboration()
        elif self.keywords.weather.wednesday == text:
            self.generals['text'] = 'weather_wednesday'
            self.elaboration()
        elif self.keywords.weather.wednesday_day == text:
            self.generals['text'] = 'weather_wednesday'
            self.generals['arg'] = 'day'
            self.elaboration()
        elif self.keywords.weather.wednesday_night == text:
            self.generals['text'] = 'weather_wednesday'
            self.generals['arg'] = 'night'
            self.elaboration()
        elif self.keywords.weather.thursday == text:
            self.generals['text'] = 'weather_thursday'
            self.elaboration()
        elif self.keywords.weather.thursday_day == text:
            self.generals['text'] = 'weather_thursday'
            self.generals['arg'] = 'day'
            self.elaboration()
        elif self.keywords.weather.thursday_night == text:
            self.generals['text'] = 'weather_thursday'
            self.generals['arg'] = 'night'
            self.elaboration()
        elif self.keywords.weather.friday == text:
            self.generals['text'] = 'weather_friday'
            self.elaboration()
        elif self.keywords.weather.friday_day == text:
            self.generals['text'] = 'weather_friday'
            self.generals['arg'] = 'day'
            self.elaboration()
        elif self.keywords.weather.friday_night == text:
            self.generals['text'] = 'weather_friday'
            self.generals['arg'] = 'night'
            self.elaboration()
        elif self.keywords.weather.saturday == text:
            self.generals['text'] = 'weather_saturday'
            self.elaboration()
        elif self.keywords.weather.saturday_day == text:
            self.generals['text'] = 'weather_saturday'
            self.generals['arg'] = 'day'
            self.elaboration()
        elif self.keywords.weather.saturday_night == text:
            self.generals['text'] = 'weather_saturday'
            self.generals['arg'] = 'night'
            self.elaboration()
        elif self.keywords.weather.sunday == text:
            self.generals['text'] = 'weather_sunday'
            self.elaboration()
        elif self.keywords.weather.sunday_day == text:
            self.generals['text'] = 'weather_sunday'
            self.generals['arg'] = 'day'
            self.elaboration()
        elif self.keywords.weather.sunday_night == text:
            self.generals['text'] = 'weather_sunday'
            self.generals['arg'] = 'night'
            self.elaboration()
        elif self.keywords.weather.pop_today == text:
            self.generals['text'] = 'pop_today'
            self.elaboration()
        elif self.keywords.weather.pop_tomorrow == text:
            self.generals['text'] = 'pop_tomorrow'
            self.elaboration()
        elif self.keywords.weather.pop_monday == text:
            self.generals['text'] = 'pop_day'
            self.generals['arg'] = 0
            self.elaboration()
        elif self.keywords.weather.pop_tuesday == text:
            self.generals['text'] = 'pop_day'
            self.generals['arg'] = 1
            self.elaboration()
        elif self.keywords.weather.pop_wednesday == text:
            self.generals['text'] = 'pop_day'
            self.generals['arg'] = 2
            self.elaboration()
        elif self.keywords.weather.pop_thursday == text:
            self.generals['text'] = 'pop_day'
            self.generals['arg'] = 3
            self.elaboration()
        elif self.keywords.weather.pop_friday == text:
            self.generals['text'] = 'pop_day'
            self.generals['arg'] = 4
            self.elaboration()
        elif self.keywords.weather.pop_saturday == text:
            self.generals['text'] = 'pop_day'
            self.generals['arg'] = 5
            self.elaboration()
        elif self.keywords.weather.pop_sunday == text:
            self.generals['text'] = 'pop_day'
            self.generals['arg'] = 6
            self.elaboration()
        elif self.keywords.weather.wind_today == text:
            self.generals['text'] = 'wind_today'
            self.elaboration()
        elif self.keywords.weather.wind_tomorrow == text:
            self.generals['text'] = 'wind_tomorrow'
            self.elaboration()
        elif self.keywords.weather.wind_monday == text:
            self.generals['text'] = 'wind_day'
            self.generals['arg'] = 0
            self.elaboration()
        elif self.keywords.weather.wind_tuesday == text:
            self.generals['text'] = 'wind_day'
            self.generals['arg'] = 1
            self.elaboration()
        elif self.keywords.weather.wind_wednesday == text:
            self.generals['text'] = 'wind_day'
            self.generals['arg'] = 2
            self.elaboration()
        elif self.keywords.weather.wind_thursday == text:
            self.generals['text'] = 'wind_day'
            self.generals['arg'] = 3
            self.elaboration()
        elif self.keywords.weather.wind_friday == text:
            self.generals['text'] = 'wind_day'
            self.generals['arg'] = 4
            self.elaboration()
        elif self.keywords.weather.wind_saturday == text:
            self.generals['text'] = 'wind_day'
            self.generals['arg'] = 5
            self.elaboration()
        elif self.keywords.weather.wind_sunday == text:
            self.generals['text'] = 'wind_day'
            self.generals['arg'] = 6
            self.elaboration()
        elif self.keywords.weather.humidity_today == text:
            self.generals['text'] = 'humidity_today'
            self.elaboration()
        elif self.keywords.weather.humidity_tomorrow == text:
            self.generals['text'] = 'humidity_tomorrow'
            self.elaboration()
        elif self.keywords.weather.humidity_monday == text:
            self.generals['text'] = 'humidity_day'
            self.generals['arg'] = 0
            self.elaboration()
        elif self.keywords.weather.humidity_tuesday == text:
            self.generals['text'] = 'humidity_day'
            self.generals['arg'] = 1
            self.elaboration()
        elif self.keywords.weather.humidity_wednesday == text:
            self.generals['text'] = 'humidity_day'
            self.generals['arg'] = 2
            self.elaboration()
        elif self.keywords.weather.humidity_thursday == text:
            self.generals['text'] = 'humidity_day'
            self.generals['arg'] = 3
            self.elaboration()
        elif self.keywords.weather.humidity_friday == text:
            self.generals['text'] = 'humidity_day'
            self.generals['arg'] = 4
            self.elaboration()
        elif self.keywords.weather.humidity_saturday == text:
            self.generals['text'] = 'humidity_day'
            self.generals['arg'] = 5
            self.elaboration()
        elif self.keywords.weather.humidity_sunday == text:
            self.generals['text'] = 'humidity_day'
            self.generals['arg'] = 6
            self.elaboration()
        else:
            self.failure()

    def section_open(self, text):
        """Check phrases from open section."""
        self.log.info('search open section')

        if self.keywords.open.open_computer == text:
            self.generals['text'] = 'open_computer'
            self.complete()
        elif self.keywords.open.open_run == text:
            self.generals['text'] = 'open_run'
            self.complete()
        elif self.keywords.open.open_charms == text:
            self.generals['text'] = 'open_charms'
            self.complete()
        elif self.keywords.open.open_settings == text:
            self.generals['text'] = 'open_settings'
            self.complete()
        elif self.keywords.open.open_share == text:
            self.generals['text'] = 'open_share'
            self.complete()
        elif self.keywords.open.open_devices == text:
            self.generals['text'] = 'open_devices'
            self.complete()
        elif ((self.keywords.open.find_application == text) or
              (self.keywords.open.find_application2 == text)):
            self.generals['text'] = 'find_application'
            self.complete()
        elif self.keywords.open.find_file == text:
            self.generals['text'] = 'find_file'
            self.complete()
        elif self.keywords.open.find_setting == text:
            self.generals['text'] = 'find_setting'
            self.complete()
        elif self.keywords.open.settings_2monitor == text:
            self.generals['text'] = 'settings_2monitor'
            self.complete()
        elif ((self.keywords.open.open_menu == text) or
              (self.keywords.open.open_menu2 == text)):
            self.generals['text'] = 'open_menu'
            self.complete()
        elif self.keywords.open.menu_system_tools == text:
            self.generals['text'] = 'menu_system_tools'
            self.complete()
        elif self.keywords.open.open_specifical_abbilities == text:
            self.generals['text'] = 'open_specifical_abbilities'
            self.complete()
        elif self.keywords.open.turn_all == text:
            self.generals['text'] = 'turn_all'
            self.complete()
        elif self.keywords.open.lock_computer == text:
            self.generals['text'] = 'lock_computer'
            self.complete()
        else:
            self.failure()

    def section_notes(self, text):
        """Check phrases from notes section."""
        self.log.info('search notes section')

        if self.keywords.notes.notes_read_titles == text:
            self.generals['text'] = 'notes_read_titles'
            self.elaboration()
        elif self.keywords.notes.notes_read == text:
            self.generals['text'] = 'notes_read'
            self.speech.speak(self.phrases.number)
            self.elaboration()
            number = recognizer2.get_number(self.stream, self.voice,
                                            self.in_speech_bf, self.keywords)
            self.generals['arg'] = number
            self.elaboration()
        elif self.keywords.notes.notes_add == text:
            self.generals['text'] = 'notes_add'
            self.complete()
        elif self.keywords.notes.notes_delete == text:
            self.speech.speak(self.phrases.number)
            self.elaboration()
            number = recognizer2.get_number(self.stream, self.voice,
                                            self.in_speech_bf, self.keywords)
            self.speech.speak(self.phrases.confirm % number)
            self.elaboration()
            check = recognizer2.confirmation(self.stream, self.voice,
                                             self.in_speech_bf, self.keywords)
            if check:
                self.generals['text'] = 'notes_delete'
                self.generals['arg'] = number
            else:
                self.speech.speak(self.phrases.good)
            self.elaboration()
        else:
            self.failure()

    def section_rss(self, text):
        """Check phrases from rss section."""
        self.log.info('search rss section')

        if not self.rss_source_flag:
            self.generals['text'] = 'rss_read_titles'
            self.speech.speak(self.phrases.source)
            self.speech.speak(self.phrases.number)
            self.elaboration()
            number = recognizer2.get_number(self.stream, self.voice,
                                            self.in_speech_bf, self.keywords)
            self.generals['arg'] = number
            self.elaboration()
            self.rss_source_flag = True
        elif self.keywords.rss.rss_read_titles == text:
            self.generals['text'] = 'rss_read_titles'
            self.elaboration()
        elif self.keywords.rss.rss_read == text:
            self.generals['text'] = 'rss_read'
            self.speech.speak(self.phrases.number)
            self.elaboration()
            number = recognizer2.get_number(self.stream, self.voice,
                                            self.in_speech_bf, self.keywords)
            self.generals['arg'] = number
            self.elaboration()
        elif self.keywords.rss.rss_open == text:
            self.generals['text'] = 'rss_open'
            self.speech.speak(self.phrases.number)
            self.elaboration()
            number = recognizer2.get_number(self.stream, self.voice,
                                            self.in_speech_bf, self.keywords)
            self.generals['arg'] = number
            self.elaboration()
        elif self.keywords.rss.rss_update == text:
            self.generals['text'] = 'rss_update'
            self.speech.speak(self.phrases.update)
            self.elaboration()
        elif self.keywords.rss.rss_next == text:
            self.generals['text'] = 'rss_next'
            self.elaboration()
        elif self.keywords.rss.rss_repeat == text:
            self.generals['text'] = 'rss_repeat'
            self.elaboration()
        elif self.keywords.rss.rss_change == text:
            self.play('disable')
            self.generals['text'] = 'rss_source'
            self.rss_source_flag = False
            self.play('enable')
        else:
            self.failure()

    def section_birthday(self, text):
        """Check phrases from birthday section."""
        self.log.info('search birthday section')

        if self.keywords.birthday.birthday_check == text:
            self.generals['text'] = 'birthday_check'
            self.elaboration()
        elif self.keywords.birthday.birthday_read == text:
            self.generals['text'] = 'birthday_read'
            self.elaboration()
        elif self.keywords.birthday.birthday_add == text:
            self.generals['text'] = 'birthday_add'
            self.complete()
        elif self.keywords.birthday.birthday_delete == text:
            self.speech.speak(self.phrases.number)
            self.elaboration()
            number = recognizer2.get_number(self.stream, self.voice,
                                            self.in_speech_bf, self.keywords)
            self.speech.speak(self.phrases.confirm % number)
            self.elaboration()
            check = recognizer2.confirmation(self.stream, self.voice,
                                             self.in_speech_bf, self.keywords)
            if check:
                self.generals['text'] = 'birthday_delete'
                self.generals['arg'] = number
            else:
                self.speech.speak(self.phrases.good)
            self.elaboration()
        elif self.keywords.birthday.birthday_update == text:
            self.generals['text'] = 'birthday_update'
            self.elaboration()
        else:
            self.failure()

    def section_events(self, text):
        """Check phrases from events section."""
        self.log.info('search events section')

        if self.keywords.events.event_check == text:
            self.generals['text'] = 'event_check'
            self.elaboration()
        elif self.keywords.events.event_read == text:
            self.generals['text'] = 'event_read'
            self.elaboration()
        elif self.keywords.events.event_add == text:
            self.generals['text'] = 'event_add'
            self.complete()
        elif self.keywords.events.event_delete == text:
            self.speech.speak(self.phrases.number)
            self.elaboration()
            number = recognizer2.get_number(self.stream, self.voice,
                                            self.in_speech_bf, self.keywords)
            self.speech.speak(self.phrases.confirm % number)
            self.elaboration()
            check = recognizer2.confirmation(self.stream, self.voice,
                                             self.in_speech_bf, self.keywords)
            if check:
                self.generals['text'] = 'event_delete'
                self.generals['arg'] = number
            else:
                self.speech.speak(self.phrases.good)
            self.elaboration()
        elif self.keywords.events.event_update == text:
            self.generals['text'] = 'event_update'
            self.elaboration()
        else:
            self.failure()

    def section_backups(self, text):
        """Check phrases from backups section."""
        self.log.info('search backups section')

        if self.keywords.backups.backup_bd == text:
            self.generals['text'] = 'backup_bd'
            self.complete()
        elif self.keywords.backups.backup_user_data == text:
            self.generals['text'] = 'backup_user_data'
            self.complete()
        elif self.keywords.backups.backup_all == text:
            self.generals['text'] = 'backup_all'
            self.complete()
        elif self.keywords.backups.restore_bd == text:
            self.generals['text'] = 'restore_bd'
            self.complete()
        elif self.keywords.backups.restore_user_data == text:
            self.generals['text'] = 'restore_user_data'
            self.complete()
        elif self.keywords.backups.restore_all == text:
            self.generals['text'] = 'restore_all'
            self.complete()
        else:
            self.failure()

    def speak_variants(self):
        """Speak variants for current search."""
        section = self.voice.get_search()

        self.play('disable')
        self.speech.speak(self.phrases.variants)
        for line in self.variants[section]:
            self.speech.speak(line.strip('\n'))
        self.play('enable')

    def elaboration(self):
        """Elaboration listening."""
        self.play('elaboration')
        self.play('enable')

    def failure(self):
        """Failure listening."""
        self.play('failure')
        self.speech.speak(self.phrases.repeat)
        self.play('enable')

    def cancel(self):
        """Cancel listening."""
        self.rss_source_flag = False
        self.voice.set_search('keyphrase')
        self.play('disable')
        self.speech.speak(self.phrases.good)

    def complete(self):
        """Complete listening."""
        self.voice.set_search('keyphrase')
        self.play('disable')

    def play(self, key):
        """Play sound used pointer method."""
        name = self.config.sounds.get(key)
        if name is not None:
            sound = os.path.join(self.config.sounds_dir, name)
            self.speech.play(sound)
