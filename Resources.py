#!/usr/bin/env python
# Written by: DGC

# python imports
import os.path
import sys

# local imports

#==============================================================================
def directory():
    """
    Returns the directory of the Resources folder.
    """
    return os.path.join(os.path.dirname(sys.argv[0]), "Resources")

#==============================================================================
if (__name__ == "__main__"):
    pass
