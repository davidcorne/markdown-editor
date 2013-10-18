#!/usr/bin/env python
# Written by: DGC

"""
Sets up the environment for integration testing.
"""

# python imports
import logging
import os
import sys

# local imports
sys.path.append("..")

import Resources
Resources.directory = lambda : os.path.dirname(__file__) + "/../Resources"

import Configuration
Configuration.user_options_file_path = lambda : os.path.dirname(__file__) + "/Options.pickle"
Configuration.default_options_file_path = lambda : os.path.dirname(__file__) + "/Options.pickle"
Configuration.user_defined_word_list_path = lambda : os.path.dirname(__file__) + "test.pwl"
Configuration.on_import()

#==============================================================================
if (__name__ == "__main__"):
    pass
