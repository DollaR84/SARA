"""
Extension for assistant of notes functions.

Created on 30.01.2017

@author: Ruslan Dolovanyuk

"""

import logging

from gui.notes import AddNote
from gui.windows import AppWindow


def if_exists(ptr, config):
    """Check exists table in database."""
    return ptr.bd.if_exists(config.name_bd, 'notes')


def setup(ptr, config):
    """Create table in database."""
    log = logging.getLogger()
    log.info('setup Sara: create notes table in database...')

    script = (
              "DROP TABLE IF EXISTS notes",
              '''CREATE TABLE notes (
                    id INTEGER PRIMARY KEY NOT NULL,
                    title TEXT NOT NULL,
                    data TEXT NOT NULL) WITHOUT ROWID
              ''',
    )
    ptr.bd.put(script)


def check(ptr, config, text, arg):
    """Check need actions for use."""
    if 'notes_read_titles' == text:
        read_titles(ptr)
    elif 'notes_read' == text:
        read(ptr, arg)
    elif 'notes_add' == text:
        add(ptr)
    elif 'notes_delete' == text:
        delete(ptr, arg)


def read_titles(ptr):
    """Read titles all notes from database."""
    log = logging.getLogger()
    log.info('read titles all notes...')

    script = 'SELECT * FROM notes'
    notes_bd = ptr.bd.get(script)

    if not notes_bd:
        ptr.speech.speak(ptr.phrases.notes.empty)

    for note in notes_bd:
        ptr.speech.speak(ptr.phrases.notes.read_title % (note[0], note[1]))


def read(ptr, num_row):
    """Read note from database."""
    log = logging.getLogger()
    log.info('read note %d' % num_row)

    notes = ptr.bd.get('SELECT * FROM notes WHERE id=%d' % num_row)
    if not notes:
        ptr.speech.speak(ptr.phrases.notes.failure % num_row)
    else:
        note = notes[0]
        ptr.speech.speak(ptr.phrases.notes.read % (note[0], note[1], note[2]))


def add(ptr):
    """Add note in database."""
    log = logging.getLogger()
    log.info('add note...')

    id_bd = 1
    note = {'title': '', 'data': ''}
    wnd = AppWindow(AddNote, ptr.phrases.gui)
    wnd.run(ptr.phrases.notes.title, note)

    if '' == note['title']:
        ptr.speech.speak(ptr.phrases.recognition.good)
    else:
        script = 'SELECT * FROM notes ORDER BY id DESC LIMIT 1'
        result = ptr.bd.get(script)
        if result:
            id_bd = result[0][0]+1

        script = '''INSERT INTO notes (id, title, data)
                    VALUES (%d, "%s", "%s")
                 ''' % (id_bd, note['title'], note['data'])
        ptr.bd.put(script)
        ptr.speech.speak(ptr.phrases.notes.add)


def delete(ptr, num_row):
    """Delete note from database."""
    log = logging.getLogger()
    log.info('delete note %d' % num_row)

    script = 'SELECT * FROM notes'
    notes_bd = ptr.bd.get(script)

    if not notes_bd:
        ptr.speech.speak(ptr.phrases.notes.empty)
    else:
        find = False
        for note in notes_bd:
            if note[0] == num_row:
                script = 'DELETE FROM notes WHERE id=%d' % note[0]
                ptr.bd.put(script)
                ptr.speech.speak(ptr.phrases.notes.delete % num_row)
                find = True
                continue

            if find:
                script = '''UPDATE notes SET id=%d WHERE id=%d
                         ''' % (note[0]-1, note[0])
                ptr.bd.put(script)

        if not find:
            ptr.speech.speak(ptr.phrases.notes.failure % num_row)
