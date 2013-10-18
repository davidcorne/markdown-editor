#!/usr/bin/env python
# Written by: DGC

# python imports
import logging
import tempfile
import time
# local imports

#==============================================================================
def __init_logfile():
    temp_file = tempfile.NamedTemporaryFile(
        prefix="Markdown_Editor_" + time.strftime("%d_%m_%y_%H_%M_"), 
        suffix=".log"
        )
    temp_file.close()
    return temp_file.name
    
#==============================================================================
def log_file(__name=__init_logfile()):
    return __name

#==============================================================================
def on_import():
    logging.basicConfig(
        filename=log_file(),
        level=logging.DEBUG,
        format="%(levelname)-7s | %(asctime)s | %(message)s",
        datefmt="%d/%m/%y %M:%H:%S"
        )
    logging.info("Started logging.")
    # only usful while debugging
    print(log_file())

on_import()

#==============================================================================
if (__name__ == "__main__"):
    pass
