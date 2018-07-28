"""
The extension recognizer module.

Created on 14.05.2017

@author: Ruslan Dolovanyuk

"""

import logging
import time


def __loop(stream, voice, in_speech_bf, keywords, func):
    """Run second loop for args."""
    result = 0
    voice.start_utt()
    while True:
        buffer = stream.read(1024)

        if buffer:
            voice.process_raw(buffer, False, False)
            if voice.get_in_speech() != in_speech_bf:
                in_speech_bf = voice.get_in_speech()

                if not in_speech_bf:
                    voice.end_utt()
                    result = func(keywords, voice.hypothesis())
                    if 0 != result:
                        break
                    voice.start_utt()
        time.sleep(0.1)
    return result


def get_number(stream, voice, in_speech_bf, keywords):
    """Get number."""
    log = logging.getLogger()
    log.info('get number...')

    old_search = voice.get_search()
    voice.set_search('digits')
    result = __loop(stream, voice, in_speech_bf, keywords.digits, digits)
    voice.set_search(old_search)
    return result


def confirmation(stream, voice, in_speech_bf, keywords):
    """Confirm question."""
    log = logging.getLogger()
    log.info('confirm question...')

    old_search = voice.get_search()
    voice.set_search('confirm')
    result = __loop(stream, voice, in_speech_bf, keywords.confirm, confirm)
    voice.set_search(old_search)

    if 1 == result:
        return True
    elif 2 == result:
        return False


def confirm(keywords, text):
    """Recognize confirm."""
    log = logging.getLogger()
    log.info('recognize confirm: %s' % text)

    if keywords.yes == text:
        return 1
    elif keywords.no == text:
        return 2


def digits(keywords, text):
    """Recognize digits."""
    log = logging.getLogger()
    log.info('recognize digit: %s' % text)

    result = 0
    numbers = text.split(' ')
    for number in numbers:
        if keywords.d1 == number:
            result += 1
        elif keywords.d2 == number:
            result += 2
        elif keywords.d3 == number:
            result += 3
        elif keywords.d4 == number:
            result += 4
        elif keywords.d5 == text:
            result += 5
        elif keywords.d6 == number:
            result += 6
        elif keywords.d7 == number:
            result += 7
        elif keywords.d8 == number:
            result += 8
        elif keywords.d9 == number:
            result += 9
        elif keywords.d10 == number:
            result += 10
        elif keywords.d11 == number:
            result += 11
        elif keywords.d12 == number:
            result += 12
        elif keywords.d13 == number:
            result += 13
        elif keywords.d14 == number:
            result += 14
        elif keywords.d15 == number:
            result += 15
        elif keywords.d16 == number:
            result += 16
        elif keywords.d17 == number:
            result += 17
        elif keywords.d18 == number:
            result += 18
        elif keywords.d19 == number:
            result += 19
        elif keywords.d20 == number:
            result += 20
        elif keywords.d30 == number:
            result += 30
        elif keywords.d40 == number:
            result += 40
        elif keywords.d50 == number:
            result += 50
        elif keywords.d60 == number:
            result += 60
        elif keywords.d70 == number:
            result += 70
        elif keywords.d80 == number:
            result += 80
        elif keywords.d90 == number:
            result += 90

    return result
