#!/usr/bin/env python
# Written by: DGC

# python imports
import unittest

# local imports
import Integration

import MarkdownEditor
import UpdaterGui
import Version

#==============================================================================
class utest_App(unittest.TestCase):
    
    @Integration.log_entry_exit
    def test_run(self):
        app = MarkdownEditor.MarkdownEditorApp([])
        editor = MarkdownEditor.MarkdownEditor([])

    @Integration.log_entry_exit
    def test_updates(self):
        app = MarkdownEditor.MarkdownEditorApp([])
        while (True):
            if (app.updater.finished):
                break

    @Integration.log_entry_exit
    def test_update_ui(self):
        Version.WINDOWS_VERSION = -1
        app = MarkdownEditor.MarkdownEditorApp([])
        while (True):
            if (app.updater.finished):
                break
        self.assertTrue(app.updater.update_available)

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
