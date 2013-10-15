#!/usr/bin/env python
# Written by: DGC

# python imports
import os.path
import sys
import unittest

# local imports
import test_utils
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

    def test_sample_markdown(self):
        path = test_utils.data_dir() + "/Markdown/Sample.md"
        assert(os.path.isfile(path))
        doc = Document(path)
        self.assertTrue(doc.saved)
        self.assertEqual(
            doc.content,
            """# Sample #

A sample of markdown.
"""
            )

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
