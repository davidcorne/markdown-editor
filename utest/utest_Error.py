#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import unittest

# local imports
sys.path.append("..")

import Error
import Exceptions

Error.set_test_mode()

#==============================================================================
class utest_Error(unittest.TestCase):
    
    def test_exception(self):
        """
        This tests that Error raises an exception, not a dialog.
        """
        modules_imported = len(sys.modules)
        self.assertRaises(
            Exceptions.TestException, 
            Error.show_error,
            "Test error."
            )
        self.assertEqual(modules_imported, len(sys.modules))

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
