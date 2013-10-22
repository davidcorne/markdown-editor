#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import unittest

# local imports
sys.path.append("..")
import Updater

#==============================================================================
class utest_Updater(unittest.TestCase):
    
    def test_get_version_from_xml(self):
        xml_string = """
<Versions>
  <Windows>1</Windows>
</Versions>
"""
        version = Updater.get_version_from_xml(xml_string)
        self.assertEqual(version, 1)
        xml_string = """
<Versions>
  <Windows>1.5</Windows>
</Versions>
"""
        version = Updater.get_version_from_xml(xml_string)
        self.assertEqual(version, 1.5)

    def test_version_xml_exists(self):
        xml = Updater.get_version_xml()
        self.assertIsNotNone(xml)

    def test_async(self):
        updater = Updater.Updater()
        while (not updater.finished):
            pass
        self.assertFalse(updater.thread.is_alive())
        self.assertTrue(updater.finished)
        
#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
