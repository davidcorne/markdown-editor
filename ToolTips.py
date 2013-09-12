#!/usr/bin/env python
# Written by: DGC

# python imports
import os
import pickle

# local imports
import Resources

#==============================================================================
def read_tool_tips():
    filename = os.path.join(Resources.directory(), "ToolTips.pickle")
    with open(filename, "rb") as tool_tips_file:
        global TOOL_TIP
        TOOL_TIP = pickle.load(tool_tips_file)

#==============================================================================
# Run on import
read_tool_tips()

#==============================================================================
if (__name__ == "__main__"):
    pass
