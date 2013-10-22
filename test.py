#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import unittest
import time

# local imports
import Log

from utest.utest_Log import *
from utest.utest_ImageConverter import *
from utest.utest_Processor import *
from utest.utest_Updater import *
from utest.utest_html import *
from utest.utest_SpellChecker import *
from utest.utest_Examples import *

try:
    from Integration.itest_ConfigurationDialog import *
    from Integration.itest_Files import *
    from Integration.itest_App import *
    from Integration.itest_Edit import *
except ImportError:
    pass

#==============================================================================
if (__name__ == "__main__"):
    start = time.time()
    retval = unittest.main(verbosity=2, exit=False)
    print("")
    with open(Log.log_file(), "r") as log_file:
        print(log_file.read())
    result = retval.result.wasSuccessful()
    message = "FAIL %s"
    if (result):
        message = "PASS %s"
        logging.getLogger("").handlers = []
        message += "\n\nRemoving log file: \"%s\"" %(Log.log_file())
        os.remove(Log.log_file())
    message = message %(": " + str(time.time() - start))
    print("")
    print(message)
    # program has succeded if exit returns 0, so pass not result
    sys.exit(not result)
