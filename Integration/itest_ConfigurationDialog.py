#!/usr/bin/env python
# Written by: DGC

# python imports
import unittest

# local imports
import Integration

import MarkdownEditor
import ConfigurationDialog

#==============================================================================
class utest_ConfigurationDialog(unittest.TestCase):
    
    @Integration.log_entry_exit
    def test_raise(self):
        app = MarkdownEditor.MarkdownEditorApp([])
        editor = MarkdownEditor.MarkdownEditor([])
        config_dialog = ConfigurationDialog.ConfigurationDialog(editor)

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)