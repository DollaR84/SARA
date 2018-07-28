"""
Load config for my scripts.

Created on 09.11.2016

@author: Ruslan Dolovanyuk

"""

import copy
import json
import logging
import os

from gui.settings import Settings
from gui.windows import AppWindow


def __load(path):

    temp_class_1 = type('__Config', (), {})
    config = temp_class_1()

    with open(path) as json_file:
        json_data = json.load(json_file)
        for name, settings in json_data.items():
            temp_class_2 = type('__' + name, (), {})
            setattr(config, name, temp_class_2())
            section = getattr(config, name)
            for key, value in settings.items():
                setattr(section, key, value)

    return config


def update(config, path):
    """Update config from user file."""
    log = logging.getLogger()
    log.info('load user config: ' + path)

    new_config = copy.deepcopy(config)
    with open(path) as json_file:
        user_config = json.load(json_file)
        for name, settings in user_config.items():
            section = getattr(new_config, name)
            for key, value in settings.items():
                if not hasattr(section, key):
                    log.error('attr not found ' + key)
                setattr(section, key, value)

    return new_config


def default():
    """Load default config."""
    log = logging.getLogger()
    log.info('load default settings...')

    filename = 'default.json'
    config = __load(filename)
    return config


def language(pathdir, code):
    """Load language from file base."""
    log = logging.getLogger()
    log.info('load language: %s...' % code)

    filename = code + '.json'
    path = os.path.join(pathdir, filename)

    lang = __load(path)
    return lang


def open_settings(ptr, config):
    """Open window settings."""
    log = logging.getLogger()
    log.info('open graphical form for change settings...')

    new_config = copy.deepcopy(config)
    content = {'save': False, 'config': new_config, 'speech': ptr.speech}
    wnd = AppWindow(Settings, ptr.phrases.gui)
    wnd.run(ptr.phrases.general.settings_title, content)

    if not content['save']:
        ptr.speech.set_voice(config.speech.voice)
        ptr.speech.set_rate(config.speech.rate)
        ptr.speech.set_volume(config.speech.volume)
        ptr.speech.speak(ptr.phrases.general.good)
    else:
        new_config.general.setup = 'false'
        config = copy.deepcopy(new_config)
        json_data = {}
        for name, section in config.__dict__.items():
            json_data[name] = section.__dict__
        json_data = json.dumps(json_data)
        replaced_data = {'{': '{\n', '}': '\n}',
                         '[': '[\n', ']': '\n]',
                         ': {': ':\n{', ': [': ':\n[',
                         ', ': ',\n'}
        for old_data, new_data in replaced_data.items():
            json_data = json_data.replace(old_data, new_data)
        json_data = offset(json_data)
        with open('user.json', 'w') as json_file:
            json_file.write(json_data)
        ptr.speech.speak(ptr.phrases.general.need_restart)


def offset(text):
    """Adding spaces offset start line in string."""
    tab = 0
    old_lines = text.split('\n')
    new_lines = []
    new_line = ''
    for old_line in old_lines:
        if ('{' == old_line[-2:]) or ('[' == old_line[-2:]):
            new_line = ' '*tab + old_line
            tab += 3
        else:
            if ((('}' == old_line[-2:]) or (']' == old_line[-2:]) or
                 ('},' == old_line[-3:]) or ('],' == old_line[-3:]))):
                tab -= 3
            new_line = ' '*tab + old_line
        new_lines.append(new_line)
    return '\n'.join(new_lines)
