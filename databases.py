"""
This module work with databases on sqlite.

Created on 21.01.2017

@author: Ruslan Dolovanyuk

"""

import logging
import os
import sqlite3
import sys


def reconnect(func):
    """Decorate methods for reconnect bd."""
    def tmp(self, *args, **kw):
        self.disconnect()
        res = func(self, *args, **kw)
        self.disconnect()
        self.connect('main')

        return res
    return tmp


class Databases:
    """The class for work databases on sqlite."""

    def __init__(self, config):
        """Initialize class for control databases."""
        self.log = logging.getLogger()
        self.log.info('initialize Databases...')
        self.log.info('version sqlite: %s' % sqlite3.version)

        self.config = config

        self.connect('main')

    def connect(self, name):
        """Connect database."""
        self.log.info('connect %s database...' % name)

        filebd = os.path.join(self.config.databases_dir,
                              self.config.databases[name])
        self.conn = sqlite3.connect(filebd)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        """Disconnect database."""
        self.log.info('disconnect database...')

        self.cursor.close()
        self.conn.close()

    def get(self, script):
        """Get data from database."""
        self.log.info('get data from database...')

        self.cursor.execute(script)
        return self.cursor.fetchall()

    @reconnect
    def get_other_bd(self, name, script):
        """Get data from other bd."""
        self.connect(name)
        return self.get(script)

    def put(self, script):
        """Set data in database."""
        self.log.info('set data in database...')

        if isinstance(script, str):
            self.cursor.execute(script)
        else:
            for line in script:
                self.cursor.execute(line)
        self.conn.commit()

    @reconnect
    def put_other_bd(self, name, script):
        """Set data in other bd."""
        self.connect(name)
        self.put(script)

    @reconnect
    def if_exists(self, name, table):
        """Check table if exist in database."""
        self.connect(name)

        str_sql = 'SELECT * FROM sqlite_master WHERE name = "%s"' % table
        self.cursor.execute(str_sql)
        if self.cursor.fetchone():
            return True
        return False

    @reconnect
    def dump(self, name, file_sql):
        """Dump database in sql file."""
        self.connect(name)
        self.log.info('dump %s database in file: %s' % (name, file_sql))

        with open(file_sql, 'w', encoding='utf-8') as sql:
            for line in self.conn.iterdump():
                sql.write('%s\n' % line)

    @reconnect
    def restore(self, name, file_sql):
        """Restore database from sql file."""
        self.connect(name)
        self.log.info('restore database %s from file: %s' % (name, file_sql))

        with open(file_sql, 'r') as sql:
            for line in sql:
                try:
                    self.cursor.execute(line)
                except:
                    self.log.info('%s %s %s' % sys.exc_info())

    def get_bd_names(self):
        """Get all names databases from config."""
        return self.config.databases.keys()
