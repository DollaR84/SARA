"""
Module have classes needed for system use.

Created on 10.01.2014

@author: Ruslan Dolovanyuk

"""

import logging
import logging.handlers
import os

from shutil import rmtree
from subprocess import PIPE
from subprocess import Popen


class Logger:
    """Class for initialization of the logging module."""

    def __init__(self, name):
        """Initialize logger class."""
        file = open(name + '.log', 'w')
        file.close()
        self.name = name
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: '
                                      '%(message)s', '%d.%m.%Y %H:%M %Ss')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        self.log.addHandler(handler)
        handler = logging.FileHandler(name + '.log', 'a')
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        self.log.addHandler(handler)
        self.log.info(">>>>> %s start <<<<<" % self.name.upper())

    def finish(self):
        """Shutdown the logger."""
        self.log.info(">>>>> %s end <<<<<" % self.name.upper())
        logging.shutdown()


class Runner:
    """Class for running other utils in command line."""

    def __init__(self):
        """Initialize runner class."""
        self.log = logging.getLogger()

    def run(self, name, run):
        """Run system utils in command line and save output."""
        process = Popen(run, stdout=PIPE, stderr=PIPE)
        output, errors = process.communicate()
        self.log.info('>>>>> ' + name + ' start <<<<<')
        self.log.error('Output:\n' + output.decode())
        self.log.error('Errors:\n' + errors.decode())
        self.log.info('>>>>> ' + name + ' end <<<<<')


class PathUtils:
    """Class wrapper for work with pathes in the file system os."""

    @staticmethod
    def clear_path(path):
        """Clear directory on the path.

        Return True if the operation was successful,
        otherwise return False.

        """
        log = logging.getLogger()
        log.info("Clear directory %s..." % (path))
        try:
            rmtree(path, True)
        except:
            log.error("Clear directory %s has failed" % (path))
            result = False
        else:
            result = True
        finally:
            return result

    @staticmethod
    def check_path(path):
        """Check path if it exists.

        Return True if path exists, otherwise return False.

        """
        log = logging.getLogger()
        result = os.path.exists(path)
        if not result:
            log.error("Path %s does not exists" % (path))
        return result

    @staticmethod
    def make_path(path):
        """Make path if it does not exist.

        Return True if the operation was successful,
        otherwise return False.

        """
        log = logging.getLogger()
        log.info("Make directory %s..." % (path))
        try:
            os.mkdir(path)
        except:
            log.error("Making directory %s has failed" % (path))
            result = False
        else:
            result = True
        finally:
            return result
