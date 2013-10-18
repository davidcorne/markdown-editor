#!/usr/bin/env python
# Written by: DGC

"""
A module to set up logging for this program.

__init_logfile() should never be used outside this module, same with 
__on_import().

You should not need this unless you need the path to the log file. That is 
gotten using log_file().

"""
# python imports
import logging
import tempfile
import time

# local imports

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
def __on_import():
    """
    Private function sets up logging. Should only be run once, on import.
    """
    logging.basicConfig(
        filename=log_file(),
        level=logging.DEBUG,
        format="%(levelname)-7s | %(asctime)s | %(message)s",
        datefmt="%d/%m/%y %M:%H:%S"
        )
    logging.info("Started logging.")
    # only usful while debugging
    print(log_file())

__on_import()

#==============================================================================
if (__name__ == "__main__"):
    pass
