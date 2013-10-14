#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import unittest

# local imports
sys.path.append("..")
from Document import *

#==============================================================================
class utest_Document(unittest.TestCase):
    
    def test_saved(self):
        doc = Document(None)
        self.assertFalse(doc.saved)
        # use __file__ so it's a real file
        doc = Document(__file__)
        self.assertTrue(doc.saved)

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
