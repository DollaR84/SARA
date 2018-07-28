"""
Speak Auto Recognition Agent.

Created on 09.11.2016

@author: Ruslan Dolovanyuk

"""

import logging
import os

from brain import Brain

from utils import Logger


if __name__ == '__main__':
    logger = Logger(os.path.splitext(__file__)[0])
    log = logging.getLogger()
    log.info('Initializing Sara...')

    brain = Brain()
    brain.mainloop()

    logger.finish()
