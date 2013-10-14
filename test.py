#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import unittest

# local imports
sys.path.append("utest")
from utest_ImageConverter import *
from utest_Processor import *
from utest_Updater import *
from utest_html import *

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
