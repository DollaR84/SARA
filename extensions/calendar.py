"""
Extension for assistant of calendar functions.

Created on 30.01.2017

@author: Ruslan Dolovanyuk

"""

import logging
import time

from datetime import datetime


def check(ptr, config, text):
    """Check need actions for use."""
    if 'time_now' == text:
        time_now(ptr, config)
    elif 'date_now' == text:
        date_now(ptr)
    elif 'date_detail' == text:
        detail(ptr)
    elif 'weekday' == text:
        weekday(ptr)


def time_now(ptr, config):
    """Get and say time now."""
    log = logging.getLogger()
    log.info('get system time')

    if 24 == config.time_format:
        strtime = time.strftime('%H:%M', time.localtime())
    elif 12 == config.time_format:
        strtime = time.strftime('%I:%M%p', time.localtime())
    else:
        strtime = ptr.phrases.calendar.format_failure
    ptr.speech.speak(ptr.phrases.calendar.now + ' ' + strtime)


def date_now(ptr):
    """Get and say date now."""
    log = logging.getLogger()
    log.info('get system date')

    strdate = time.strftime('%d.%m.%Y', time.localtime())
    ptr.speech.speak(ptr.phrases.calendar.today + ' ' + strdate)
    weekday(ptr)


def detail(ptr):
    """Get and say detail information of date."""
    log = logging.getLogger()
    log.info('detail information of today date...')

    date_now(ptr)
    isodate = datetime.today().isocalendar()
    ptr.speech.speak(ptr.phrases.calendar.isoweek % isodate[1])
    ptr.speech.speak(ptr.phrases.calendar.isoday % isodate[2])
    ptr.speech.speak(ptr.phrases.calendar.dayyear %
                     int(time.strftime('%j', time.localtime())))


def weekday(ptr):
    """Get and say weekday."""
    log = logging.getLogger()
    log.info('get week day...')

    ptr.speech.speak(ptr.phrases.calendar.weekday[datetime.today().weekday()])
