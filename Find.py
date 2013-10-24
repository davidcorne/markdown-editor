#!/usr/bin/env python
# Written by: DGC

# python imports

from PyQt4 import QtGui

# local imports

from UserText import USER_TEXT

#==============================================================================
class FindDialog(QtGui.QDockWidget):

    def __init__(self, parent):
        super(FindDialog, self).__init__(
            USER_TEXT["find_title"],
            parent
            )
        self.move(parent.frameGeometry().center())
        tabs = QtGui.QTabWidget(self)
        tabs.setTabsClosable(False)
        
        find_widget = FindReplaceWidget(parent.editor, self.close)
        replace_widget = FindReplaceWidget(
            parent.editor,
            self.close,
            replace=True
            )
        tabs.addTab(find_widget, USER_TEXT["find_title"])
        tabs.addTab(replace_widget, USER_TEXT["replace_title"])

        self.setWidget(tabs)
        self.topLevelChanged.connect(self.adjustSize)
        self.setFloating(True)

#==============================================================================
class FindReplaceWidget(QtGui.QWidget):

    def __init__(self, editor, close_action, replace=False):
        super(FindReplaceWidget, self).__init__()
       
        self.editor = editor
        self.close_action = close_action
        self.replace_widget = replace

        self.find_backwards = False
        self.find_case_sensitive = False
        self.find_whole_words = False
        
        self.initialise_ui()

    def initialise_ui(self):
        find_label = QtGui.QLabel(USER_TEXT["find_what"])
        self.find_entry = QtGui.QLineEdit()
        self.find_entry.returnPressed.connect(self.find)
        find_label.setBuddy(self.find_entry)
       
        replace_label = QtGui.QLabel(USER_TEXT["replace_with"])
        self.replace_entry = QtGui.QLineEdit()
        self.replace_entry.returnPressed.connect(self.find)
        replace_label.setBuddy(self.replace_entry)

        case_box = QtGui.QCheckBox(USER_TEXT["match_case"])
        case_box.stateChanged.connect(self.find_case_changed)
        
        backward_box = QtGui.QCheckBox(
            USER_TEXT["search_backwards"]
            )
        backward_box.stateChanged.connect(self.find_backwards_changed)

        whole_words_box = QtGui.QCheckBox(
            USER_TEXT["match_whole_words"]
            )
        whole_words_box.stateChanged.connect(self.find_whole_words_changed)
        
        find_button = QtGui.QPushButton(
            USER_TEXT["find"]
            )
        find_button.clicked.connect(self.find)
        
        replace_button = QtGui.QPushButton(
            USER_TEXT["replace"]
            )
        replace_button.clicked.connect(self.replace)
        replace_all_button = QtGui.QPushButton(
            USER_TEXT["replace_all"]
            )
        replace_all_button.clicked.connect(self.replace_all)

        close_button = QtGui.QPushButton(USER_TEXT["close"])
        close_button.clicked.connect(self.close_action)

        find_layout = QtGui.QHBoxLayout()
        find_layout.addWidget(find_label)
        find_layout.addWidget(self.find_entry)

        replace_layout = QtGui.QHBoxLayout()
        replace_layout.addWidget(replace_label)
        replace_layout.addWidget(self.replace_entry)

        replace_buttons = QtGui.QHBoxLayout()
        replace_buttons.addWidget(replace_button)
        replace_buttons.addWidget(replace_all_button)

        left_layout = QtGui.QVBoxLayout()
        left_layout.addLayout(find_layout)
        if (self.replace_widget):
            left_layout.addLayout(replace_layout)
        left_layout.addWidget(case_box)
        left_layout.addWidget(backward_box)
        left_layout.addWidget(whole_words_box)
        left_layout.addStretch()
        
        right_layout = QtGui.QVBoxLayout()
        right_layout.addWidget(find_button)
        if (self.replace_widget):
            right_layout.addLayout(replace_buttons)
        right_layout.addWidget(close_button)
        right_layout.addStretch()
        
        main_layout = QtGui.QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)
       
    def find_case_changed(self):
        self.find_case_sensitive = not self.find_case_sensitive

    def find_backwards_changed(self):
        self.find_backwards = not self.find_backwards

    def find_whole_words_changed(self):
        self.find_whole_words = not self.find_whole_words

    def get_find_flags(self):
        """
        Returns the flags or'd together.
        """
        flags = QtGui.QTextDocument.FindFlags()
        if (self.find_backwards):
            flags = flags | QtGui.QTextDocument.FindBackward
        if (self.find_case_sensitive):
            flags = flags | QtGui.QTextDocument.FindCaseSensitively
        if (self.find_whole_words):
            flags = flags | QtGui.QTextDocument.FindWholeWords
        return flags

    def find(self, raise_dialog=True):
        found = False
        if (self.editor.count()):
            text = self.find_entry.text()
            found = self.editor.currentWidget().text.find(
                text,
                self.get_find_flags()
                )
            if (found):
                self.editor.currentWidget().activateWindow()
                self.editor.currentWidget().text.setFocus()
            elif (raise_dialog):
                cant_find_dialog = QtGui.QMessageBox(
                    QtGui.QMessageBox.Information,
                    "Not Found",
                    "The following specified text was not found:",
                    QtGui.QMessageBox.Ok,
                    self
                    ) 
                cant_find_dialog.setInformativeText(text)
                cant_find_dialog.show()
        return found

    def replace(self, raise_dialog=True):
        text = self.replace_entry.text()
        cursor = self.editor.currentWidget().text.textCursor()
        # check if we have already found what we want
        # check if there is highlighted text
        if (cursor.selectedText() == text):
            found = True
        else:
            found = self.find(raise_dialog)
        if (found):
            # the cursor should be highlighting the found text
            cursor.insertText(text)
        return found

    def replace_all(self):
        while(self.replace(raise_dialog=False)):
            pass
        
#==============================================================================
if (__name__ == "__main__"):
    pass
