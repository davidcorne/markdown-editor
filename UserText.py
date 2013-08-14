#!/usr/bin/env python
# Written by: DGC

# python imports
import os
import pickle

# local imports
import Resources

#==============================================================================
def read_user_text():
    filename = os.path.join(Resources.directory(), "UserText.pickle")
    with open(filename, "rb") as user_text_file:
        global USER_TEXT
        USER_TEXT = pickle.load(user_text_file)

#==============================================================================
# Run on import
read_user_text()

#==============================================================================
if (__name__ == "__main__"):
    pass
