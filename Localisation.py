#!/usr/bin/env python
# Written by: DGC

# python imports
import os
import pickle

# local imports
import Resources

#==============================================================================
def language_directory():
    """
    Returns the Language directory.
    """
    return os.path.join(Resources.directory(), "Languages")

#==============================================================================
def language_options_file():
    """
    Returns the Language options file.
    """
    return os.path.join(Resources.directory(), "Languages", "Languages.pickle")

#==============================================================================
class Localiser(object):

    def __init__(self, language_file=language_options_file()):
        self.listeners = list()
        self.language_file = language_file
        with open(self.language_file, "r") as options_file:
            self.options = pickle.load(options_file)

    def language(self):
        return self.options["language"]

    def set_language(self, language):
        available_languages = self.options["available_languages"]
        if (language not in available_languages):
            raise KeyError("%s was not found in available languages: %s" %(
                language, 
                str(available_languages),
              )
            )
        self.options["language"] = language
        self.write_options()
        self.notify()

    def write_options(self):
        with open(self.language_file, "wb") as options_file:
            pickle.dump(self.options, options_file)

    def notify(self):
        for listener in self.listeners:
            listener.language_changed()            

#==============================================================================
if (__name__ == "__main__"):
    pass
