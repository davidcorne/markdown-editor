#!/usr/bin/env python
# Written by: DGC

# python imports
import os
import logging
import sys

# local imports
sys.path.append(".")
sys.path.append("..")

import Log
# immediately stop logging
logging.getLogger("").handlers = []

#==============================================================================
def main():
    log_directory = os.path.dirname(Log.log_file())
    print("Removing: ")
    for temp_file in os.listdir(log_directory):
        if ("Markdown_Editor_" in temp_file and temp_file[-4:] == ".log"):
            file_path = os.path.join(log_directory, temp_file)
            print(file_path)
            os.remove(file_path)

#==============================================================================
if (__name__ == "__main__"):
    main()
