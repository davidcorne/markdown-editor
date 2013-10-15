#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import unittest

# local imports
import test_utils

sys.path.append("..")
from SpellChecker import *

#==============================================================================
class utest_SpellChecker(unittest.TestCase):
    
    def test_location(self):
        dict_dir = test_utils.data_dir() + "/Languages"
        d = Dict("dgc", dict_dir)
        
#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
