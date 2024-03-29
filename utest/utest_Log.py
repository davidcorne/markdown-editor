#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import logging
import unittest

# local imports
sys.path.append("..")
import Log

LOG = Log.log_file()

#==============================================================================
class utest_Log(unittest.TestCase):
    
    def test_exception(self):
        thrown = False
        try:
            Log.__init_logfile()
        except AttributeError:
            thrown = True
        self.assertTrue(thrown)

    def test_the_same(self):
        path_1 = Log.log_file()
        path_2 = Log.log_file()
        self.assertEqual(path_1, path_2)
        self.assertEqual(LOG, path_1)

    def test_always_the_same(self):
        self.assertEqual(LOG, Log.log_file())
        
    def test_cant_change_name(self):
        new_path = Log.log_file(__name="new")
        path = Log.log_file()
        self.assertNotEqual(new_path, path)
        self.assertEqual(path, LOG)

    def test_log(self):
        Log.start_logging()
        logging.debug("test_log: Test 1")
        logging.info("test_log: Test 2")
        logging.warning("test_log: Test 3")
        with open(LOG, "r") as log_file:
            content = log_file.read()
        self.assertIn("DEBUG", content)
        self.assertIn("test_log: Test 1", content)

        self.assertIn("INFO", content)
        self.assertIn("test_log: Test 2", content)

        self.assertIn("WARNING", content)
        self.assertIn("test_log: Test 3", content)

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
