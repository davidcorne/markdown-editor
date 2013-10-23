#!/usr/bin/env python
# Written by: DGC

"""
A module to set up logging for this program.

__init_logfile() should never be used outside this module.

You should not need this unless you need the path to the log file. That is 
gotten using log_file().

"""
# python imports
import logging
import tempfile
import time
import sys

# local imports

LOG_FORMAT = "%(levelname)-7s | %(asctime)s | %(message)s"
LOG_TIME_FORMAT = "%d/%m/%y %M:%H:%S"

#==============================================================================
def __init_logfile():
    """
    Private function to create a temporary log file.
    Returns the path to the log file.
    """
    temp_file = tempfile.NamedTemporaryFile(
        prefix="Markdown_Editor_" + time.strftime("%d_%m_%y_%H_%M_"), 
        suffix=".log"
        )
    temp_file.close()
    return temp_file.name
    
#==============================================================================
def log_file(__name=__init_logfile()):
    """
    Function to return the path to the log file. This has a private argument 
    __name which is evaluated on import. This acts as a private global variable
    so this will always return the correct log file, never create a new one.
    """
    return __name

#==============================================================================
def add_file_log(path, log_format=LOG_FORMAT, log_time_format=LOG_TIME_FORMAT):
    file_logger = logging.FileHandler(path)
    formatter = logging.Formatter(log_format, log_time_format)
    file_logger.setFormatter(formatter)
    logging.getLogger('').addHandler(file_logger)

#==============================================================================
def add_console_log(log_format=LOG_FORMAT, log_time_format=LOG_TIME_FORMAT):
    """
    Add a handler to the default logger to write messages to std::out
    """
    console = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(log_format, log_time_format)
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

#==============================================================================
def start_logging():
    """
    Private function sets up logging. Should only be run once.
    """
    log_file_path = log_file()
    # only usful while debugging
    print(log_file_path)
    print("")
    logger = logging.getLogger("")
    logger.handlers = []
    logger.setLevel(logging.DEBUG)
    add_file_log(log_file_path)
    add_console_log()
    logging.info("Started logging.")

#==============================================================================
if (__name__ == "__main__"):
    pass
