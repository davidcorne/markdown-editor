#!/usr/bin/env python
# Written by: DGC

# python imports
import unittest

from PyQt4 import QtGui

# local imports
import Integration

import MarkdownEditor

#==============================================================================
class utest_Edit(unittest.TestCase):
    
    @Integration.log_entry_exit
    def test_italise(self):
        app = MarkdownEditor.MarkdownEditorApp([])
        editor = MarkdownEditor.MarkdownEditor([])
        editor.new_file()
        document_frame = editor.editor.currentWidget()
        document = document_frame.text
        document.setText("In the test THIS word will be made italic")
        cursor = document.textCursor()
        cursor.setPosition(14)
        cursor.select(QtGui.QTextCursor.WordUnderCursor)
        document.setTextCursor(cursor)
        word = cursor.selectedText()
        self.assertEqual(str(word), "THIS")
        editor.italic_highlighted()
        text = str(document.toPlainText())
        self.assertEqual(text, "In the test _THIS_ word will be made italic")

    @Integration.log_entry_exit
    def test_bold(self):
        app = MarkdownEditor.MarkdownEditorApp([])
        editor = MarkdownEditor.MarkdownEditor([])
        editor.new_file()
        document_frame = editor.editor.currentWidget()
        document = document_frame.text
        document.setText("In the test THIS word will be made bold")
        cursor = document.textCursor()
        cursor.setPosition(14)
        cursor.select(QtGui.QTextCursor.WordUnderCursor)
        document.setTextCursor(cursor)
        word = cursor.selectedText()
        self.assertEqual(str(word), "THIS")
        editor.bold_highlighted()
        text = str(document.toPlainText())
        self.assertEqual(text, "In the test __THIS__ word will be made bold")

    @Integration.log_entry_exit
    def test_colour(self):
        app = MarkdownEditor.MarkdownEditorApp([])
        editor = MarkdownEditor.MarkdownEditor([])
        editor.new_file()
        document_frame = editor.editor.currentWidget()
        document = document_frame.text
        document.setText("In the test THIS word will be made red")
        cursor = document.textCursor()
        cursor.setPosition(14)
        cursor.select(QtGui.QTextCursor.WordUnderCursor)
        document.setTextCursor(cursor)
        word = cursor.selectedText()
        self.assertEqual(str(word), "THIS")
        editor.colour_highlighted("red")
        text = str(document.toPlainText())
        self.assertEqual(
            text, 
            "In the test <font color=\"red\">THIS</font> word will be made red"
            )

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
