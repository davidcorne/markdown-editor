#!/usr/bin/env python
# Written by: DGC

# python imports
import unittest

# local imports
import Integration

import Main

#==============================================================================
class utest_Files(unittest.TestCase):
    
    @Integration.log_entry_exit
    def test_new_file(self):
        app = Main.run([])
        editor = app.editor
        self.assertEqual(editor.editor.count(), 0)
        editor.new_file()
        self.assertEqual(editor.editor.count(), 1)
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

    @Integration.log_entry_exit
    def test_close_tabs(self):
        app = Main.run([])
        editor = app.editor
        editor.new_file()
        editor.tab_close_requested(0)
        self.assertEqual(editor.editor.count(), 0)
        
        # make 6 new tabs
        editor.new_file()
        editor.new_file()
        editor.new_file()
        editor.new_file()
        editor.new_file()
        editor.new_file()
        self.assertEqual(editor.editor.count(), 6)
        # we are on the last tab
        self.assertEqual(editor.editor.currentIndex(), 5)
        editor.tab_close_requested(0)
        # close the first tab, we are on index 4
        self.assertEqual(editor.editor.currentIndex(), 4)
        # more to tab index 2
        editor.editor.setCurrentIndex(2)
        editor.tab_close_requested(4)
        # close a tab to the right, our index doesn't change
        self.assertEqual(editor.editor.currentIndex(), 2)
        # close a tab to our left, our index decrements
        editor.tab_close_requested(0)
        self.assertEqual(editor.editor.currentIndex(), 1)
        editor.tab_close_requested(1)
        # close our tab, if there are tabs to the right our index is the same
        self.assertEqual(editor.editor.currentIndex(), 1)
        editor.tab_close_requested(1)
        self.assertEqual(editor.editor.currentIndex(), 0)
        editor.tab_close_requested(0)
        # we have deleted them all
        self.assertEqual(editor.editor.count(), 0)

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
