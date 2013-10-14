#!/usr/bin/env python
# Written by: DGC

# python imports
import unittest

# local imports
from Document import *

#==============================================================================
class utest_Document(unittest.TestCase):
    
    def test_saved(self):
        doc = Document(None)
        self.assertFalse(doc.saved)

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
