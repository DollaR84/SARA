"""
Control backups Sara databases and user datas.

Created on 22.01.2017

@author: Ruslan Dolovanyuk

"""

import logging
import os
import tarfile


class Backups:
    """Class for backups databases and user data."""

    def __init__(self, config, bd):
        """Initialize class for backups databases and user data."""
        self.log = logging.getLogger()
        self.log.info('initialize Backups...')

        self.config = config
        self.bd = bd

    def pack(self, name, path):
        """Packing user data in archive."""
        self.log.info('packing %s in %s.tar.gz' % (path, name))

        arc_name = os.path.join(self.config.backups_dir, name + '.tar.gz')
        arc = tarfile.open(arc_name, 'w:gz')
        arc.add(path)
        arc.close()

    def unpack(self, name, path):
        """Unpack user data from archive."""
        self.log.info('unpack %s.tar.gz in %s' %
                      (name, os.path.split(path)[0]))

        arc_name = os.path.join(self.config.backups_dir, name + '.tar.gz')
        arc = tarfile.open(arc_name, 'r')
        arc.extractall('%s/' % os.path.splitdrive(path)[0])
        arc.close()

    def backup_bd(self):
        """Backup all databases."""
        self.log.info('backup all databases...')

        for base in self.bd.get_bd_names():
            file_name = base + '.sql'
            file_path = os.path.join(self.config.backups_dir, file_name)
            self.bd.dump(base, file_path)

    def backup_user_data(self):
        """Backup user data."""
        self.log.info('backup all user datas...')

        for name, path in self.config.user_data.items():
            self.pack(name, path)

    def backup_all(self):
        """Backup all data."""
        self.backup_bd()
        self.backup_user_data()

    def restore_bd(self):
        """Restore all databases."""
        self.log.info('restore all databases...')

        for base in self.bd.get_bd_names():
            file_name = base + '.sql'
            file_path = os.path.join(self.config.backups_dir, file_name)
            self.bd.restore(base, file_path)

    def restore_user_data(self):
        """Restore user data from archive."""
        self.log.info('restore all user data...')

        for name, path in self.config.user_data.items():
            self.unpack(name, path)

    def restore_all(self):
        """Restore all data."""
        self.restore_bd()
        self.restore_user_data()
