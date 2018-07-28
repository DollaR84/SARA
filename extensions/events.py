"""
Extension for assistant of events functions.

Created on 14.02.2017

@author: Ruslan Dolovanyuk

"""

import json
import logging
import os

from datetime import date

from gui.events import AddEvent
from gui.windows import AppWindow


def if_exists(ptr, config):
    """Check exists table in database."""
    return ptr.bd.if_exists(config.name_bd, 'events')


def setup(ptr, config):
    """Create table in database."""
    log = logging.getLogger()
    log.info('setup Sara: create events table in database...')

    script = (
              "DROP TABLE IF EXISTS events",
              '''CREATE TABLE events (
                    id INTEGER PRIMARY KEY NOT NULL,
                    event TEXT NOT NULL,
                    day INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    year INTEGER) WITHOUT ROWID
              ''',
    )
    ptr.bd.put(script)

    update(ptr, config)


def update(ptr, config):
    """Update database from file."""
    log = logging.getLogger()
    log.info('update data events from file in database...')

    file_name = os.path.join(config.file_path, config.file_name)
    if not os.path.exists(file_name):
        return

    with open(file_name, 'r') as json_file:
        json_data = json.load(json_file)

        id_bd = 1
        script = 'SELECT * FROM events ORDER BY id DESC LIMIT 1'
        result = ptr.bd.get(script)
        if result:
            id_bd = result[0][0]+1
        script = []
        bd_data = ptr.bd.get('SELECT * FROM events')
        for line in json_data:
            find = False
            for data in bd_data:
                if data[1] == line[0]:
                    find = True
                    break

            if not find:
                str_line = '''INSERT INTO events (id, event, day, month, year)
                              VALUES (%d, "%s", %d, %d, %d)
                           ''' % (id_bd, line[0], line[1], line[2], line[3])
                script.append(str_line)
                id_bd += 1

        ptr.bd.put(script)
        ptr.speech.speak(ptr.phrases.general.update)


def check(ptr, config, text, arg):
    """Check need actions for use."""
    if 'event_check' == text:
        notice(ptr)
    elif 'event_read' == text:
        read(ptr)
    elif 'event_add' == text:
        add(ptr)
    elif 'event_delete' == text:
        delete(ptr, arg)
    elif 'event_update' == text:
        update(ptr, config)


def notice(ptr):
    """Check and say events from database."""
    today = date.today()
    data = ptr.bd.get('SELECT * FROM events')
    for line in data:
        date_event = date(today.year, line[3], line[2])
        delta = date_event - today

        if 0 <= delta.days <= 1:
            ptr.notice()

        if 1 == delta.days:
            ptr.speech.speak(ptr.phrases.events.tomorrow % (line[1],
                                                            line[2],
                                                            line[3],
                                                            line[4]))
        elif 0 == delta.days:
            ptr.speech.speak(ptr.phrases.events.today % (line[1],
                                                         line[2],
                                                         line[3],
                                                         line[4]))


def read(ptr):
    """Read all events in database."""
    log = logging.getLogger()
    log.info('read all events in database...')
    script = 'SELECT * FROM events'
    data_db = ptr.bd.get(script)

    if not data_db:
        ptr.speech.speak(ptr.phrases.events.empty)

    for data in data_db:
        ptr.speech.speak(ptr.phrases.events.read_all % (data[0], data[1]))


def add(ptr):
    """Add event in database."""
    log = logging.getLogger()
    log.info('add event...')

    id_bd = 1
    event = {'date': '', 'data': ''}
    wnd = AppWindow(AddEvent, ptr.phrases.gui)
    wnd.run(ptr.phrases.events.title, event)

    if '' == event['data']:
        ptr.speech.speak(ptr.phrases.recognition.good)
    else:
        script = 'SELECT * FROM events ORDER BY id DESC LIMIT 1'
        result = ptr.bd.get(script)
        if result:
            id_bd = result[0][0]+1

        date = event['date'].split('.')
        script = '''INSERT INTO events (id, event, day, month, year)
                    VALUES (%d, "%s", %d, %d, %d)
                 ''' % (id_bd, event['data'],
                        int(date[0]), int(date[1]), int(date[2]))
        ptr.bd.put(script)
        ptr.speech.speak(ptr.phrases.events.add)


def delete(ptr, num_row):
    """Delete event from database."""
    log = logging.getLogger()
    log.info('delete event %d' % num_row)

    script = 'SELECT * FROM events'
    events_bd = ptr.bd.get(script)

    if not events_bd:
        ptr.speech.speak(ptr.phrases.events.empty)
    else:
        find = False
        for event in events_bd:
            if event[0] == num_row:
                script = 'DELETE FROM events WHERE id=%d' % event[0]
                ptr.bd.put(script)
                ptr.speech.speak(ptr.phrases.events.delete % num_row)
                find = True
                continue

            if find:
                script = '''UPDATE events SET id=%d WHERE id=%d
                         ''' % (event[0]-1, event[0])
                ptr.bd.put(script)

        if not find:
            ptr.speech.speak(ptr.phrases.events.failure % num_row)
