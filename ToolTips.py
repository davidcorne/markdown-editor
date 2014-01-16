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
        tool_tips = pickle.load(tool_tips_file)
    return tool_tips

#==============================================================================
# Run on import
TOOL_TIP = read_tool_tips()

#==============================================================================
if (__name__ == "__main__"):
    pass
