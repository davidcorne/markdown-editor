#!/usr/bin/env python
# Written by: DGC

# python imports
import os
import pickle
import logging

# local imports
import Resources

#==============================================================================
def read_user_text(locale):
    filename = os.path.join(
        Resources.directory(), 
        "Languages",
        locale,
        "UserText.pickle"
    )
    logging.info("Read user text from %s", filename)
    with open(filename, "rb") as user_text_file:
        user_text = pickle.load(user_text_file)
    return user_text

#==============================================================================
# Run on import
USER_TEXT = read_user_text("en_GB")
keys = sorted(USER_TEXT.keys())
for i in keys:
    print i + ",", USER_TEXT[i]

#==============================================================================
if (__name__ == "__main__"):
    pass
