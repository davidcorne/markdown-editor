#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import unittest

# local imports
import Integration

import Log
import MarkdownEditor

#==============================================================================
class utest_Integration(unittest.TestCase):
    
    def test_run(self):
        app = MarkdownEditor.MarkdownEditorApp([])
        editor = MarkdownEditor.MarkdownEditor([])

    def test_updates(self):
        app = MarkdownEditor.MarkdownEditorApp([])
        while (True):
            if (app.updater.finished):
                break

    def test_new_file(self):
        app = MarkdownEditor.MarkdownEditorApp([])
        editor = MarkdownEditor.MarkdownEditor([])
        editor.new_file()
        document_frame = editor.editor.currentWidget()
        document = document_frame.text
        document.setText("""
# Test #

This is a test of markdown.
""")
        view = document_frame.output
        html = view.page().mainFrame().toHtml()
        self.assertIn("<h1>Test</h1>", html)
        self.assertIn("<p>This is a test of markdown.</p>", html)
        self.assertEqual(html.count("<h1>"), 1)
        self.assertEqual(html.count("</h1>"), 1)
        self.assertEqual(html.count("<p>"), 1)
        self.assertEqual(html.count("</p>"), 1)

    def test_close_tab(self):
        app = MarkdownEditor.MarkdownEditorApp([])
        editor = MarkdownEditor.MarkdownEditor([])
        editor.new_file()
        editor.tab_close_requested(0)
        self.assertEqual(editor.editor.count(), 0)

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
