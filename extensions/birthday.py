"""
Extension for assistant of birthday functions.

Created on 22.01.2017

@author: Ruslan Dolovanyuk

"""

import json
import logging
import os

from datetime import date

from gui.birthday import AddBirthday
from gui.windows import AppWindow


def if_exists(ptr, config):
    """Check exists table in database."""
    return ptr.bd.if_exists(config.name_bd, 'birthday')


def setup(ptr, config):
    """Create table in database."""
    log = logging.getLogger()
    log.info('setup Sara: create birthday table in database...')

    script = (
              "DROP TABLE IF EXISTS birthday",
              '''CREATE TABLE birthday (
                    id INTEGER PRIMARY KEY NOT NULL,
                    firstname TEXT NOT NULL,
                    lastname TEXT NOT NULL,
                    day INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    year INTEGER,
                    category TEXT) WITHOUT ROWID
              ''',
    )
    ptr.bd.put(script)

    update(ptr, config)


def update(ptr, config):
    """Update database from file."""
    log = logging.getLogger()
    log.info('update data birthdays from file in database...')

    file_name = os.path.join(config.file_path, config.file_name)
    if not os.path.exists(file_name):
        return

    with open(file_name, 'r') as json_file:
        json_data = json.load(json_file)

        id_bd = 1
        script = 'SELECT * FROM birthday ORDER BY id DESC LIMIT 1'
        result = ptr.bd.get(script)
        if result:
            id_bd = result[0][0]+1
        script = []
        bd_data = ptr.bd.get('SELECT * FROM birthday')
        for line in json_data:
            find = False
            for data in bd_data:
                if (data[1] == line[0]) and (data[2] == line[1]):
                    find = True
                    break

            if not find:
                str_line = '''INSERT INTO birthday
                              (id, firstname, lastname,
                               day,month, year, category)
                              VALUES (%d, "%s", "%s", %d, %d, %d, "%s")
                           ''' % (id_bd, line[0], line[1],
                                  line[2], line[3], line[4], line[5])
                script.append(str_line)
                id_bd += 1

        ptr.bd.put(script)
        ptr.speech.speak(ptr.phrases.general.update)


def check(ptr, config, text, arg):
    """Check need actions for use."""
    if 'birthday_check' == text:
        notice(ptr)
    elif 'birthday_read' == text:
        read(ptr)
    elif 'birthday_add' == text:
        add(ptr)
    elif 'birthday_delete' == text:
        delete(ptr, arg)
    elif 'birthday_update' == text:
        update(ptr, config)


def notice(ptr):
    """Check date today with date from database."""
    today = date.today()
    data = ptr.bd.get('SELECT * FROM birthday')
    for line in data:
        dr = date(today.year, line[4], line[3])
        delta = dr - today

        if 0 <= delta.days <= 3:
            ptr.notice()
            if jubilee(ptr, line, delta.days):
                continue

        if 3 >= delta.days > 1:
            ptr.speech.speak(ptr.phrases.birthday.before % (line[1],
                                                            line[2],
                                                            delta.days))
        elif 1 == delta.days:
            ptr.speech.speak(ptr.phrases.birthday.tomorrow % (line[1],
                                                              line[2]))
        elif 0 == delta.days:
            ptr.speech.speak(ptr.phrases.birthday.today % (line[1], line[2]))


def jubilee(ptr, line, days):
    """Check dates on jubilee."""
    if 0 == line[5]:
        return False

    years = date.today().year - line[5]
    if 0 == (years % 5):
        if 3 >= days > 1:
            ptr.speech.speak(ptr.phrases.jubilee.before % (line[1],
                                                           line[2],
                                                           days,
                                                           years))
            return True
        elif 1 == days:
            ptr.speech.speak(ptr.phrases.jubilee.tomorrow % (line[1],
                                                             line[2],
                                                             years))
            return True
        elif 0 == days:
            ptr.speech.speak(ptr.phrases.jubilee.today % (line[1],
                                                          line[2],
                                                          years))
            return True
    return False


def read(ptr):
    """Read all birthday in database."""
    log = logging.getLogger()
    log.info('read all birthday in database...')
    script = 'SELECT * FROM birthday'
    data_db = ptr.bd.get(script)

    if not data_db:
        ptr.speech.speak(ptr.phrases.birthday.empty)

    for data in data_db:
        ptr.speech.speak(ptr.phrases.birthday.read_all % (data[0], data[1],
                                                          data[2]))


def add(ptr):
    """Add birthday in database."""
    log = logging.getLogger()
    log.info('add birthday...')

    id_bd = 1
    birthday = {'firstname': '', 'lastname': '', 'date': '',
                'category': ptr.phrases.birthday.category, 'index': 2}
    wnd = AppWindow(AddBirthday, ptr.phrases.gui)
    wnd.run(ptr.phrases.birthday.title, birthday)

    if (('' == birthday['firstname']) and ('' == birthday['lastname'])):
        ptr.speech.speak(ptr.phrases.recognition.good)
    else:
        script = 'SELECT * FROM birthday ORDER BY id DESC LIMIT 1'
        result = ptr.bd.get(script)
        if result:
            id_bd = result[0][0]+1

        date = birthday['date'].split('.')
        script = '''INSERT INTO birthday (id, firstname, lastname, day, month, year, category)
                    VALUES (%d, "%s", "%s", %d, %d, %d, "%s")
                 ''' % (id_bd, birthday['firstname'], birthday['lastname'],
                        int(date[0]), int(date[1]), int(date[2]),
                        birthday['category'][birthday['index']])
        ptr.bd.put(script)
        ptr.speech.speak(ptr.phrases.birthday.add)


def delete(ptr, num_row):
    """Delete birthday from database."""
    log = logging.getLogger()
    log.info('delete birthday %d' % num_row)

    script = 'SELECT * FROM birthday'
    birthday_bd = ptr.bd.get(script)

    if not birthday_bd:
        ptr.speech.speak(ptr.phrases.birthday.empty)
    else:
        find = False
        for birthday in birthday_bd:
            if birthday[0] == num_row:
                script = 'DELETE FROM birthday WHERE id=%d' % birthday[0]
                ptr.bd.put(script)
                ptr.speech.speak(ptr.phrases.birthday.delete % num_row)
                find = True
                continue

            if find:
                script = '''UPDATE birthday SET id=%d WHERE id=%d
                         ''' % (birthday[0]-1, birthday[0])
                ptr.bd.put(script)

        if not find:
            ptr.speech.speak(ptr.phrases.birthday.failure % num_row)
