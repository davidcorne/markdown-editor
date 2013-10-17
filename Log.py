#!/usr/bin/env python
# Written by: DGC

# python imports
import logging
import tempfile
import time
# local imports

LOG_FILE = ""

#==============================================================================
def on_import():
    temp_file = tempfile.NamedTemporaryFile(
        prefix="Markdown_Editor_" + time.strftime("%M_%H_%d_%m_%y_"), 
        suffix=".log"
        )
    temp_file.close()
    global LOG_FILE
    LOG_FILE = temp_file.name
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.DEBUG,
        format="%(levelname)-7s | %(asctime)s | %(message)s",
        datefmt="%d/%m/%y %M:%H:%S"
        )
    logging.info("Started logging.")
    # only usful while debugging
    print(LOG_FILE)

on_import()

#==============================================================================
if (__name__ == "__main__"):
    pass
