#!/usr/bin/env python
# Written by: DGC

# python imports
import unittest

# local imports
from utest.utest_Log import *
from utest.utest_ImageConverter import *
from utest.utest_Processor import *
from utest.utest_Updater import *
from utest.utest_html import *
from utest.utest_SpellChecker import *

try:
    from Integration.utest_Integration import *
except ImportError:
    pass

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
