
#!/usr/bin/env python
# Written by: DGC

"""
Sets up the environment for integration testing.
"""

# python imports
import logging
import os
import sys

# local imports
sys.path.append("..")

import Resources
Resources.directory = lambda : os.path.join(
    os.path.dirname(__file__),
    "..",
    "Resources"
    )

# now we've setup the resource path we can setup the environment.
import SetupEnv

import Error
Error.set_test_mode()

import Log
Log.start_logging()
logger = logging.getLogger("")
logger.handlers = []
Log.add_file_log(Log.log_file())

import Configuration

Configuration.user_options_file_path = lambda : os.path.dirname(__file__) + "/Options.pickle"
Configuration.default_options_file_path = lambda : os.path.dirname(__file__) + "/Options.pickle"
Configuration.user_defined_word_list_path = lambda : os.path.dirname(__file__) + "/test.pwl"
Configuration.on_import()

#==============================================================================
def log_entry_exit(test_func):
    #==========================================================================
    def wrapper(*args):
        logging.info("Entering: \"%s\"", test_func.__name__)
        res = test_func(*args)
        logging.info("Exiting: \"%s\"\n\n", test_func.__name__)
        return res
    return wrapper

#==============================================================================
def data_file(path):
    """
    Finds the file under /data/
    """
    return os.path.join(os.path.dirname(__file__), "data", path)

#==============================================================================
if (__name__ == "__main__"):
    pass
