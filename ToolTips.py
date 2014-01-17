#!/usr/bin/env python
# Written by: DGC

# python imports
import os
import pickle
import logging

# local imports
import Resources

#==============================================================================
class ToolTip(dict):

    def __init__(self, locale):
        self.read(locale)

    def read(self, locale):
        filename = os.path.join(
            Resources.directory(), 
            "Languages",
            locale,
            "ToolTips.pickle"
        )
        logging.info("Read tool tips from %s", filename)
        with open(filename, "rb") as tool_tips_file:
            tool_tips = pickle.load(tool_tips_file)
        for key in tool_tips:
            self[key] = tool_tips[key]       

    def language_changed(self, locale):
        self.read(locale)

#==============================================================================
# will be set later
TOOL_TIP = dict()

#==============================================================================
if (__name__ == "__main__"):
    pass
