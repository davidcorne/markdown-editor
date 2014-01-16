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
def read_tool_tip(locale):
    filename = os.path.join(
        Resources.directory(), 
        "Languages",
        locale,
        "ToolTips.pickle"
    )
    logging.info("Read tool tips from %s", filename)
    with open(filename, "rb") as tool_tip_file:
        tool_tip = pickle.load(tool_tip_file)
    return tool_tip

#==============================================================================
def set_tool_tip():
    global TOOL_TIP
    localiser = Localisation.Localiser()
    TOOL_TIP = read_tool_tip(localiser.language())

#==============================================================================
# Run on import
set_tool_tip()

#==============================================================================
if (__name__ == "__main__"):
    pass
