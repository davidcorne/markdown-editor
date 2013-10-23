#!/usr/bin/env python
# Written by: DGC

# python imports
import unittest

# local imports
import Integration

import Main
import Version

#==============================================================================
class utest_App(unittest.TestCase):
    
    @Integration.log_entry_exit
    def test_run(self):
        app = Main.run([])

    @Integration.log_entry_exit
    def test_updates(self):
        app = Main.run([])
        while (True):
            if (app.updater.finished):
                break

    @Integration.log_entry_exit
    def test_update_ui(self):
        Version.WINDOWS_VERSION = -1
        app = Main.run([])
        while (True):
            if (app.updater.finished):
                break
        self.assertTrue(app.updater.update_available)

    @Integration.log_entry_exit
    def test_help(self):
        app = Main.run([])
        editor = app.editor
        editor.help.markdown_description()
        editor.help.markdown_extra_description()
        editor.help.markdown_all_description()
        editor.help.codehilite_description()
        editor.help.github_description()

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
