#!/usr/bin/env python
# Written by: DGC

# python imports
import os
import sys
import tempfile
import unittest

# local imports
import test_utils

sys.path.append("..")
from SpellChecker import *

#==============================================================================
class utest_SpellChecker(unittest.TestCase):
    DICT_DIR = test_utils.data_dir() + "/Languages"

    def test_location(self):
        path = tempfile.NamedTemporaryFile().name
        d = Dict("dgc", self.DICT_DIR, path)
        os.remove(path)

    def test_pwl(self):
        path = "test.pwl"
        checker = Dict("dgc", self.DICT_DIR, path)
        test_word = "abcdefg"
        self.assertFalse(checker.dict.check(test_word))
        checker.dict.add(test_word)
        self.assertTrue(checker.dict.check(test_word))
        os.remove(path)

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
