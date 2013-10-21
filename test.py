#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import unittest

# local imports
import Log

from utest.utest_Log import *
from utest.utest_ImageConverter import *
from utest.utest_Processor import *
from utest.utest_Updater import *
from utest.utest_html import *
from utest.utest_SpellChecker import *

try:
    from Integration.utest_Files import *
    from Integration.utest_App import *
    from Integration.utest_Edit import *
except ImportError:
    pass

#==============================================================================
if (__name__ == "__main__"):
    retval = unittest.main(verbosity=2, exit=False)
    print("")
    with open(Log.log_file(), "r") as log_file:
        print(log_file.read())
    result = retval.result.wasSuccessful()
    if (result):
        print("PASS")
    else:
        print("FAIL")
    # program has succeded if exit returns 0, so pass not result
    sys.exit(not result)
