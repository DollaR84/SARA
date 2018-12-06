"""
The speak module.

Created on 26.11.2016

@author: Ruslan Dolovanyuk

"""

import ctypes
import logging
import sys
import time
import winsound

import win32com.client


class Speech:
    """The speak class for speak voice."""

    def __init__(self, config):
        """Initialize speech class."""
        self.log = logging.getLogger()
        self.log.info('initialize speech...')

        self.config = config

        self.SVSFlagsAsync = 1
        self.speaker = win32com.client.Dispatch("Sapi.SpVoice")
        self.voices = self.speaker.GetVoices()
        self.voices_ids = [voice.Id for voice in self.voices]
        self.voices_names = [voice.GetDescription() for voice in self.voices]

        self.set_voice(self.config.voice)
        self.speaker.Rate = self.config.rate
        self.speaker.Volume = self.config.volume

        self.log.info('load nvdaControllerClient32.dll...')
        self.nvda = True if self.config.nvda == "true" else False
        self.nvda_error = False
        self.sLib = ctypes.windll.LoadLibrary('./nvdaControllerClient32.dll')
        nvda_error = self.sLib.nvdaController_testIfRunning()
        errorMessage = str(ctypes.WinError(nvda_error))
        if 0 != nvda_error:
            self.log.error(errorMessage)
            self.log.error('Error communicating with NVDA')
            self.nvda_error = True

        self.set_speak_out()

    def set_voice(self, index):
        """Set voice for speak."""
        self.log.info('set voice sapi: %s' % self.voices_names[index])
        try:
            self.speaker.Voice = self.voices[index]
            self.speak_sapi(self.voices_names[index])
        except:
            self.log.error('do not change voice')

    def set_rate(self, value):
        """Change rate voice."""
        self.log.info('set rate sapi: %d' % value)
        self.speaker.Rate = value
        self.speak_sapi(str(value))

    def set_volume(self, value):
        """Change volume voice."""
        self.log.info('set volume sapi: %d' % value)
        self.speaker.Volume = value
        self.speak_sapi(str(value))

    def set_speak_out(self):
        """Set speak out: nvda or sapi."""
        self.log.info('change speak out: nvda or sapi...')
        if self.nvda and not self.nvda_error:
            self.speak = self.speak_nvda
            self.abort = self.abort_nvda
        else:
            self.speak = self.speak_sapi
            self.abort = self.abort_sapi

    def speak_nvda(self, phrase):
        """Speak phrase in nvda screen reader."""
        self.log.info('speak phrase: %s' % phrase)
        self.sLib.nvdaController_speakText(phrase)

        shift = len(phrase) // 5
        timeout = shift * 0.5
        time.sleep(timeout)

    def speak_sapi(self, phrase):
        """Speak phrase in sapi voice."""
        self.log.info('speak phrase: %s' % phrase)
        self.speaker.Speak(phrase, self.SVSFlagsAsync)
        time.sleep(0.1)

    def abort_nvda(self):
        """Abort speak nvda."""
        self.log.info('abort speak nvda...')
        self.sLib.nvdaController_cancelSpeech()

    def abort_sapi(self):
        """Abort speak sapi."""
        self.log.info('abort speak sapi...')
        self.speaker.skip("Sentence", sys.maxsize)

    def play(self, sound):
        """Play sound in sound lib."""
        self.log.info('play sound: %s' % sound)

        winsound.PlaySound(sound, winsound.SND_FILENAME)
