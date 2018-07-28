"""
Extension for assistant of rss functions.

Created on 06.08.2017

@author: Ruslan Dolovanyuk

"""

import logging
import re
import webbrowser

import feedparser


def if_exists(ptr, config):
    """Check exists table in database."""
    for index, feed in enumerate(config.feeds, 1):
        if not ptr.bd.if_exists(config.name_bd, 'table%d' % index):
            return False
    return True


def setup(ptr, config):
    """Create tables in database."""
    log = logging.getLogger()
    log.info('setup Sara: create rss tables in database...')

    for index, feed in enumerate(config.feeds, 1):
        script = (
                  "DROP TABLE IF EXISTS table%d" % index,
                  '''CREATE TABLE table%d (
                        id INTEGER PRIMARY KEY NOT NULL,
                        title TEXT NOT NULL,
                        summary TEXT NOT NULL,
                        link TEXT NOT NULL) WITHOUT ROWID
                  ''' % index,
        )
        ptr.bd.put_other_bd(config.name_bd, script)


def delete_table(ptr, config, index):
    """Delete table from rss database."""
    script = 'DROP TABLE IF EXISTS table%d' % index
    ptr.bd.put_other_bd(config.name_bd, script)


def check(ptr, config, text, arg):
    """Check need actions for use."""
    if 'rss_source' == text:
        source(ptr, config)
    elif 'rss_read_titles' == text:
        if arg is not None:
            if arg > len(ptr.rss_source):
                ptr.rss_source = ptr.rss_source[0]
            else:
                ptr.rss_source = ptr.rss_source[arg-1]
        else:
            read_titles(ptr, config)
    elif 'rss_read' == text:
        read(ptr, config, arg)
    elif 'rss_open' == text:
        open_link(ptr, config, arg)
    elif 'rss_update' == text:
        update(ptr, config)
    elif 'rss_next' == text:
        ptr.rss_next = True
        read_titles(ptr, config)
    elif 'rss_repeat' == text:
        read_titles(ptr, config)


def source(ptr, config):
    """Set and speak all sources in rss database."""
    log = logging.getLogger()
    log.info('set and read all feeds...')

    ptr.rss_start = 1
    ptr.rss_source = config.feeds
    for index, feed in enumerate(ptr.rss_source, 1):
        ptr.speech.speak(ptr.phrases.rss.source % (index, feed[0]))


def read_titles(ptr, config):
    """Read titles all rss from database."""
    log = logging.getLogger()
    log.info('read titles all rss...')

    ptr.speech.speak(ptr.rss_source[0])
    index = __get_num_table(config, ptr.rss_source[0])
    script = 'SELECT * FROM table%d' % index
    entries = ptr.bd.get_other_bd(config.name_bd, script)
    if not entries:
        ptr.speech.speak(ptr.phrases.rss.empty)

    start = ptr.rss_start+5 if ptr.rss_next else ptr.rss_start
    for index, entry in enumerate(entries, 1):
        if (index < start) or (index >= start+5):
            continue
        ptr.speech.speak(ptr.phrases.rss.read_title % (entry[0], entry[1]))

    if ptr.rss_next:
        ptr.rss_start += 5
    ptr.rss_next = False


def read(ptr, config, num_row):
    """Read rss from database."""
    log = logging.getLogger()
    log.info('read rss %d' % num_row)

    index = __get_num_table(config, ptr.rss_source[0])
    script = 'SELECT * FROM table%d WHERE id=%d' % (index, num_row)
    entries = ptr.bd.get_other_bd(config.name_bd, script)
    if not entries:
        ptr.speech.speak(ptr.phrases.rss.failure % num_row)
    else:
        entry = entries[0]
        ptr.speech.speak(ptr.phrases.rss.read % (entry[0], entry[1], entry[2]))


def open_link(ptr, config, num_row):
    """Open rss link from database."""
    log = logging.getLogger()
    log.info('open rss link %d' % num_row)

    index = __get_num_table(config, ptr.rss_source[0])
    script = 'SELECT * FROM table%d WHERE id=%d' % (index, num_row)
    entries = ptr.bd.get_other_bd(config.name_bd, script)
    if not entries:
        ptr.speech.speak(ptr.phrases.rss.failure % num_row)
    else:
        webbrowser.open(entries[0][3])


def update(ptr, config):
    """Update all feeds in rss database."""
    log = logging.getLogger()
    log.info('update all feeds in rss database cache...')

    for index, feed in enumerate(config.feeds, 1):
        data = feedparser.parse(feed[1])
        script = 'DELETE FROM table%d' % index
        ptr.bd.put_other_bd(config.name_bd, script)

        num_row = 1
        list_rows = []
        for entry in data['entries']:
            title = __get_format_string(entry['title'])
            summary = __get_format_string(entry['summary'])
            script = '''INSERT INTO table%d (id, title, summary, link)
                        VALUES (%d, "%s", "%s", "%s")
                     ''' % (index, num_row, title, summary, entry['link'])
            list_rows.append(script)
            num_row += 1
        ptr.bd.put_other_bd(config.name_bd, list_rows)


def __get_num_table(config, feed_name):
    """Return index table in database from name feed."""
    for index, feed in enumerate(config.feeds, 1):
        if feed[0] == feed_name:
            return index


def __get_format_string(in_str):
    """Return format string."""
    pattern = re.compile(r'\<[^>]*\>')
    out_str = in_str.encode('utf-8').decode('utf-8')
    out_str = out_str.replace('"', '""')
    out_str = pattern.sub('', out_str)
    return out_str
