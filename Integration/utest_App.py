#!/usr/bin/env python
# Written by: DGC

# python imports
import unittest

# local imports
import Integration

import MarkdownEditor

#==============================================================================
class utest_App(unittest.TestCase):
    
    def test_run(self):
        app = MarkdownEditor.MarkdownEditorApp([])
        editor = MarkdownEditor.MarkdownEditor([])

    def test_updates(self):
        app = MarkdownEditor.MarkdownEditorApp([])
        while (True):
            if (app.updater.finished):
                break

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
