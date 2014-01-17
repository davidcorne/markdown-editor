#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import os
import shutil
import unittest

# local imports
import test_utils

sys.path.append("..")
from Localisation import *

#==============================================================================
def temp_data(name):
    """
    Copies the Languages.pickle file so writing doesn't affect the original.
    """
    original = test_utils.data_dir() + "/Languages/Languages.pickle"
    shutil.copyfile(original, name)
    return name
    
#==============================================================================
class utest_Localisation(unittest.TestCase):
    #==========================================================================
    class Listener(object):
            
        def __init__(self):
            self.notified = False
            
        def language_changed(self, language):
            self.notified = True
    
    def test_language(self):
        localiser = Localiser(
            test_utils.data_dir() + "/Languages/Languages.pickle"
        )
        self.assertEqual(localiser.language(), "en_GB")
        self.assertEqual(
            localiser.options["available_languages"], 
            ["en_GB", "de_DE", "en_AU", "en_US", "fr_FR"]
        )

    def test_notify(self):
        localiser = Localiser(
            test_utils.data_dir() + "/Languages/Languages.pickle"
        )
        listener = self.Listener()
        localiser.listeners.append(listener)
        localiser.notify()
        self.assertTrue(listener.notified)

    def test_set_language(self):
        temp_file = temp_data("test_set_language.pickle")
        localiser = Localiser(temp_file)
        self.assertNotEqual(localiser.language(), "en_US")
        localiser.set_language("en_US")
        self.assertEqual(localiser.language(), "en_US")
    
        listener = self.Listener()
        localiser.listeners.append(listener)
        self.assertFalse(listener.notified)
        localiser.set_language("en_US")
        self.assertTrue(listener.notified)

        self.assertRaises(KeyError, localiser.set_language, "foo")
        os.remove(temp_file)

    def test_persistence(self):
        temp_file = temp_data("test_persistence.pickle")
        localiser_1 = Localiser(temp_file)
        self.assertEqual(localiser_1.language(), "en_GB")
        localiser_1.set_language("fr_FR")
        
        localiser_2 = Localiser(temp_file)
        self.assertEqual(localiser_2.language(), "fr_FR")
        os.remove(temp_file)

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
