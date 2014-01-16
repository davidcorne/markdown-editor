#!/usr/bin/env python
# Written by: DGC

# python imports
import os
import pickle
import logging

# local imports
import Resources
import Localisation

#==============================================================================
class UserText(dict):

    def __init__(self, locale):
        self.read(locale)

    def read(self, locale):
        filename = os.path.join(
            Resources.directory(), 
            "Languages",
            locale,
            "UserText.pickle"
        )
        logging.info("Read user text from %s", filename)
        with open(filename, "rb") as user_text_file:
            user_text = pickle.load(user_text_file)
        for key in user_text:
            self[key] = user_text[key]       

    def language_changed(self, locale):
        self.read(locale)

#==============================================================================
if (__name__ == "__main__"):
    pass
