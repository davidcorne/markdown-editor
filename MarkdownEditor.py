#! /usr/bin/python

# python imports

import copy
import sys
import os
import markdown

from PyQt4 import QtGui, QtCore

# local imports

import Configuration

#==============================================================================
class MarkdownEditor(QtGui.QMainWindow):

    def __init__(self, files):
        """
        files is an iterable of files to open.
        """
        super(MarkdownEditor, self).__init__()
        
        self.editor = QtGui.QTabWidget(self)
        self.editor.setTabsClosable(True)
        self.editor.tabCloseRequested.connect(self.tab_close_requested)
        self.initialise_UI()
        self.setCentralWidget(self.editor)
        
        for markdown in files:
            try:
                self.open_file(markdown)
            except IOError as e:
                error = "".join(
                    [
                        "File \"",
                        markdown,
                        "\" does not exist"
                        ]
                    )
                QtGui.QMessageBox.critical(
                    self,
                    "Error",
                    error
                    )

    def tab_close_requested(self, index):
        old_index = self.editor.currentIndex()
        self.editor.setCurrentIndex(index)
        self.close_file()
        # old_index should decrement if you've deleted a tab left of it
        if (index < old_index):
            old_index -= 1
        self.editor.setCurrentIndex(old_index)

    def initialise_UI(self):
        self.create_menu()
        self.create_toolbars()
        status_bar = QtGui.QStatusBar()
        self.setStatusBar(status_bar)
        
        self.setWindowTitle(Configuration.USER_TEXT["program_name"])
        self.resize(1200, 600)
        self.centre()
        self.show()

    def closeEvent(self, event):
        all_closed = True
        while (self.editor.count()):
            if (not self.close_file()):
                all_closed = False
                break
        if (all_closed):
            event.accept()
        else:
            event.ignore()

    def centre(self):
        """ Centre the window in the screen. """
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_toolbars(self):
        self.create_file_toolbar()
        self.create_edit_toolbar()
        self.create_undo_redo_toolbar()
        self.create_format_toolbar()

    def create_undo_redo_toolbar(self):
        undo_redo_toolbar = QtGui.QToolBar(
            Configuration.USER_TEXT["undo_redo_toolbar"]
            )

        undo_button = QtGui.QToolButton()
        undo_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["undo"])
            )
        undo_button.setToolTip(Configuration.TOOL_TIP["undo"])
        undo_button.setStatusTip(Configuration.TOOL_TIP["undo"])
        undo_button.clicked.connect(self.undo)

        redo_button = QtGui.QToolButton()
        redo_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["redo"])
            )
        redo_button.setToolTip(Configuration.TOOL_TIP["redo"])
        redo_button.setStatusTip(Configuration.TOOL_TIP["redo"])
        redo_button.clicked.connect(self.redo)

        undo_redo_toolbar.addWidget(undo_button)
        undo_redo_toolbar.addWidget(redo_button)

        # now change the undo_redo toolbar properties
        undo_redo_toolbar.setMovable(True)
        undo_redo_toolbar.setFloatable(True)
        undo_redo_toolbar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.addToolBar(undo_redo_toolbar)

    def create_format_toolbar(self):
        format_toolbar = QtGui.QToolBar(
            Configuration.USER_TEXT["format_toolbar"]
            )

        bold_button = QtGui.QToolButton()
        bold_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["bold"])
            )
        bold_button.setToolTip(Configuration.TOOL_TIP["bold"])
        bold_button.setStatusTip(Configuration.TOOL_TIP["bold"])
        bold_button.clicked.connect(self.bold_highlighted)

        italic_button = QtGui.QToolButton()
        italic_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["italic"])
            )
        italic_button.setToolTip(Configuration.TOOL_TIP["italic"])
        italic_button.setStatusTip(Configuration.TOOL_TIP["italic"])
        italic_button.clicked.connect(self.italic_highlighted)

        code_button = QtGui.QToolButton()
        code_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["code"])
            )
        code_button.setToolTip(Configuration.TOOL_TIP["code"])
        code_button.setStatusTip(Configuration.TOOL_TIP["code"])
        code_button.clicked.connect(self.code_highlighted)

        colour_button = ColourButton(self, self.colour_highlighted)

        format_toolbar.addWidget(bold_button)
        format_toolbar.addWidget(italic_button)
        format_toolbar.addWidget(code_button)
        format_toolbar.addWidget(colour_button)

        # now change the format toolbar properties
        format_toolbar.setMovable(True)
        format_toolbar.setFloatable(True)
        format_toolbar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.addToolBar(format_toolbar)

    def create_file_toolbar(self):
        file_toolbar = QtGui.QToolBar(
            Configuration.USER_TEXT["file_toolbar"]
            )

        # add the buttons
        new_button = QtGui.QToolButton()
        new_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["new_file"])
            )
        new_button.setToolTip(Configuration.TOOL_TIP["new_file"])
        new_button.setStatusTip(Configuration.TOOL_TIP["new_file"])
        new_button.clicked.connect(self.new_file)

        save_button = QtGui.QToolButton()
        save_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["save_file"])
            )
        save_button.setToolTip(Configuration.TOOL_TIP["save_file"])
        save_button.setStatusTip(Configuration.TOOL_TIP["save_file"])
        save_button.clicked.connect(self.save_file)

        open_button = QtGui.QToolButton()
        open_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["open_file"])
            )
        open_button.setToolTip(Configuration.TOOL_TIP["open_file"])
        open_button.setStatusTip(Configuration.TOOL_TIP["open_file"])
        open_button.clicked.connect(self.query_open_file)

        save_all_button = QtGui.QToolButton()
        save_all_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["save_all"])
            )
        save_all_button.setToolTip(Configuration.TOOL_TIP["save_all"])
        save_all_button.setStatusTip(Configuration.TOOL_TIP["save_all"])
        save_all_button.clicked.connect(self.save_all_files)

        close_button = QtGui.QToolButton()
        close_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["close_file"])
            )
        close_button.setToolTip(Configuration.TOOL_TIP["close_file"])
        close_button.setStatusTip(Configuration.TOOL_TIP["close_file"])
        close_button.clicked.connect(self.close_file)

        export_html_button = QtGui.QToolButton()
        export_html_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["export_html"])
            )
        export_html_button.setToolTip(Configuration.TOOL_TIP["export_html"])
        export_html_button.setStatusTip(Configuration.TOOL_TIP["export_html"])
        export_html_button.clicked.connect(self.export_html)

        file_toolbar.addWidget(new_button)
        file_toolbar.addWidget(open_button)
        file_toolbar.addWidget(save_button)
        file_toolbar.addWidget(save_all_button)
        file_toolbar.addWidget(close_button)
        file_toolbar.addWidget(export_html_button)

        # now change the file toolbar properties
        file_toolbar.setMovable(True)
        file_toolbar.setFloatable(True)
        file_toolbar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.addToolBar(file_toolbar)

    def create_edit_toolbar(self):
        edit_toolbar = QtGui.QToolBar(
            Configuration.USER_TEXT["edit_toolbar"]
            )

        # add the buttons
        cut_button = QtGui.QToolButton()
        cut_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["cut"])
            )
        cut_button.setToolTip(Configuration.TOOL_TIP["cut"])
        cut_button.setStatusTip(Configuration.TOOL_TIP["cut"])
        cut_button.clicked.connect(self.cut)

        copy_button = QtGui.QToolButton()
        copy_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["copy"])
            )
        copy_button.setToolTip(Configuration.TOOL_TIP["copy"])
        copy_button.setStatusTip(Configuration.TOOL_TIP["copy"])
        copy_button.clicked.connect(self.copy)

        paste_button = QtGui.QToolButton()
        paste_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["paste"])
            )
        paste_button.setToolTip(Configuration.TOOL_TIP["paste"])
        paste_button.setStatusTip(Configuration.TOOL_TIP["paste"])
        paste_button.clicked.connect(self.paste)

        edit_toolbar.addWidget(cut_button)
        edit_toolbar.addWidget(copy_button)
        edit_toolbar.addWidget(paste_button)

        # now change the edit toolbar properties
        edit_toolbar.setMovable(True)
        edit_toolbar.setFloatable(True)
        edit_toolbar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.addToolBar(edit_toolbar)

    def create_menu(self):
        self.create_file_menu()
        self.create_edit_menu()
        self.create_tools_menu()

    def create_edit_menu(self):
        undo_action = QtGui.QAction(Configuration.USER_TEXT["undo"], self)
        undo_action.setIcon(QtGui.QIcon(Configuration.IMAGES["undo"]))
        undo_action.setStatusTip(Configuration.TOOL_TIP["undo"])
        undo_action.triggered.connect(self.undo)

        redo_action = QtGui.QAction(Configuration.USER_TEXT["redo"], self)
        redo_action.setIcon(QtGui.QIcon(Configuration.IMAGES["redo"]))
        redo_action.setStatusTip(Configuration.TOOL_TIP["redo"])
        redo_action.triggered.connect(self.redo)

        cut_action = QtGui.QAction(Configuration.USER_TEXT["cut"], self)
        cut_action.setIcon(QtGui.QIcon(Configuration.IMAGES["cut"]))
        cut_action.setStatusTip(Configuration.TOOL_TIP["cut"])
        cut_action.triggered.connect(self.cut)

        copy_action = QtGui.QAction(Configuration.USER_TEXT["copy"], self)
        copy_action.setIcon(QtGui.QIcon(Configuration.IMAGES["copy"]))
        copy_action.setStatusTip(Configuration.TOOL_TIP["copy"])
        copy_action.triggered.connect(self.copy)

        paste_action = QtGui.QAction(Configuration.USER_TEXT["paste"], self)
        paste_action.setIcon(QtGui.QIcon(Configuration.IMAGES["paste"]))
        paste_action.setStatusTip(Configuration.TOOL_TIP["paste"])
        paste_action.triggered.connect(self.paste)

        select_all_action = QtGui.QAction(
            Configuration.USER_TEXT["select_all"],
            self
            )
        select_all_action.setStatusTip(Configuration.TOOL_TIP["select_all"])
        select_all_action.triggered.connect(self.select_all)

        search_action = QtGui.QAction(
            Configuration.USER_TEXT["find_and_replace"], 
            self
            )
        search_action.setIcon(QtGui.QIcon(Configuration.IMAGES["find"]))
        search_action.setShortcut("Ctrl+F")
        search_action.setStatusTip(Configuration.TOOL_TIP["find_and_replace"])
        search_action.triggered.connect(self.raise_find_dialog)

        menu_bar = self.menuBar()
        edit_menu = menu_bar.addMenu(Configuration.USER_TEXT["edit_menu"])
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(select_all_action)
        edit_menu.addAction(search_action)

    def create_tools_menu(self):
        configure_action = QtGui.QAction(
            Configuration.USER_TEXT["configure"], 
            self
            )
        configure_action.setIcon(
            QtGui.QIcon(Configuration.IMAGES["configure"])
            )
        configure_action.setStatusTip(Configuration.TOOL_TIP["configure"])
        configure_action.triggered.connect(self.raise_configure_dialog)

        menu_bar = self.menuBar()
        tools_menu = menu_bar.addMenu(Configuration.USER_TEXT["tools_menu"])
        tools_menu.addAction(configure_action)

    def create_file_menu(self):
        new_action = QtGui.QAction(Configuration.USER_TEXT["new_file"], self)
        new_action.setIcon(QtGui.QIcon(Configuration.IMAGES["new_file"]))
        new_action.setShortcut("Ctrl+N")
        new_action.setStatusTip(Configuration.TOOL_TIP["new_file"])
        new_action.triggered.connect(self.new_file)

        save_action = QtGui.QAction(Configuration.USER_TEXT["save_file"], self)
        save_action.setIcon(QtGui.QIcon(Configuration.IMAGES["save_file"]))
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip(Configuration.TOOL_TIP["save_file"])
        save_action.triggered.connect(self.save_file)

        save_as_action = QtGui.QAction(
            Configuration.USER_TEXT["save_as"],
            self
            )
        save_as_action.setIcon(QtGui.QIcon(Configuration.IMAGES["save_as"]))
        save_as_action.setShortcut("F12")
        save_as_action.setStatusTip(Configuration.TOOL_TIP["save_as"])
        save_as_action.triggered.connect(self.save_file_as)

        save_all_action =  QtGui.QAction(
            Configuration.USER_TEXT["save_all"],
            self
            )
        save_all_action.setIcon(QtGui.QIcon(Configuration.IMAGES["save_all"]))
        save_all_action.setShortcut("Ctrl+Shift+S")
        save_all_action.setStatusTip(Configuration.TOOL_TIP["save_all"])
        save_all_action.triggered.connect(self.save_all_files)

        open_action = QtGui.QAction(Configuration.USER_TEXT["open_file"], self)
        open_action.setIcon(QtGui.QIcon(Configuration.IMAGES["open_file"]))
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip(Configuration.TOOL_TIP["open_file"])
        open_action.triggered.connect(self.query_open_file)

        close_action = QtGui.QAction(
            Configuration.USER_TEXT["close_file"],
            self
            )
        close_action.setIcon(QtGui.QIcon(Configuration.IMAGES["close_file"]))
        close_action.setShortcut("Ctrl+F4")
        close_action.setStatusTip(Configuration.TOOL_TIP["close_file"])
        close_action.triggered.connect(self.close_file)

        export_action = QtGui.QAction(
            Configuration.USER_TEXT["export_html"], 
            self
            )
        export_action.setIcon(QtGui.QIcon(Configuration.IMAGES["export_html"]))
        export_action.setStatusTip(Configuration.TOOL_TIP["export_html"])
        export_action.triggered.connect(self.export_html)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu(Configuration.USER_TEXT["file_menu"])
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)
        file_menu.addSeparator()
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(save_all_action)
        file_menu.addSeparator()
        file_menu.addAction(export_action)

    def raise_configure_dialog(self):
        config_dialog = ConfigurationDialog(self)
        if (self.editor.count()):
            self.editor.currentWidget().reload()

    def raise_find_dialog(self):
        find_dialog = FindDialog(self)

    def colour_highlighted(self, colour):
        if (self.editor.count()):
            self.editor.currentWidget().colour_highlighted(colour)

    def bold_highlighted(self):
        if (self.editor.count()):
            self.editor.currentWidget().bold_highlighted()

    def italic_highlighted(self):
        if (self.editor.count()):
            self.editor.currentWidget().italic_highlighted()

    def code_highlighted(self):
        if (self.editor.count()):
            self.editor.currentWidget().code_block_highlighted()

    def cut(self):
        if (self.editor.count()):
            self.editor.currentWidget().text.cut()

    def copy(self):
        if (self.editor.count()):
            self.editor.currentWidget().text.copy()

    def paste(self):
        if (self.editor.count()):
            self.editor.currentWidget().text.paste()

    def undo(self):
        if (self.editor.count()):
            self.editor.currentWidget().text.undo()

    def redo(self):
        if (self.editor.count()):
            self.editor.currentWidget().text.redo()

    def select_all(self):
        if (self.editor.count()):
            self.editor.currentWidget().text.selectAll()

    def new_file(self):
        document = Document(None, self.document_changed)
        self.editor.addTab(document, "")
        self.editor.setCurrentIndex(self.editor.count() - 1)
        self.set_tab_title()

    def export_html(self):
        if (self.editor.count()):
            file_path = QtGui.QFileDialog.getSaveFileName(
                self,
                "Export HTML",
                ".",
                "HTML (*.html)"
                )
            if (file_path):
                self.editor.currentWidget().export_html(file_path)

    def close_file(self):
        if (not self.editor.count()):
            # there is no tab, so close the program
            self.close()
        else:
            if (not self.editor.currentWidget().saved):
                # have a dialog here for saving current tab
                # do you want to save the changes you've made to [file_path]
                # yes/no/cancel
                 confirm_dialog = QtGui.QMessageBox()
                 message = "".join(
                     [
                       "You have made changes to ",
                       self.editor.currentWidget().filename
                       ]
                     )
                 confirm_dialog.setText(message)
                 confirm_dialog.setInformativeText(
                     "Do you want to save your changes?"
                     )
                 confirm_dialog.setStandardButtons(
                     QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel
                     )
                 confirm_dialog.setDefaultButton(QtGui.QMessageBox.Save);
                 ret_val = confirm_dialog.exec_();
                 if (ret_val == QtGui.QMessageBox.Save):
                     self.save_file()
                 elif (ret_val == QtGui.QMessageBox.Cancel):
                     return False
            self.editor.removeTab(self.editor.currentIndex())
            return True

    def save_file_as(self):
        if (self.editor.count()):
            file_path = QtGui.QFileDialog.getSaveFileName(
                self,
                "Save As",
                ".",
                Configuration.MARKDOWN_FILE_STRING
                )
            if (file_path):
                self.editor.currentWidget().file_path = file_path
                self.editor.currentWidget().save_file()
                self.set_tab_title()
                self.statusBar().showMessage(
                    Configuration.USER_TEXT["saved"],
                    1000
                    )

    def save_file(self):
        if (self.editor.count()):
            if (self.editor.currentWidget().file_path):
                self.editor.currentWidget().save_file()
            else:
                self.save_file_as()
            self.set_tab_title()
            self.statusBar().showMessage(
                Configuration.USER_TEXT["saved"], 
                1000
                )

    def save_all_files(self):
        current_index = self.editor.currentIndex()
        for index in range(self.editor.count()):
            self.editor.setCurrentIndex(index)
            self.save_file()
        self.editor.setCurrentIndex(current_index)
            
    def query_open_file(self):
        file_path = QtGui.QFileDialog.getOpenFileName(
            self,
            "Open File",
            ".",
            Configuration.MARKDOWN_FILE_STRING
            )
        if (file_path):
            self.open_file(file_path)

    def open_file(self, file_path):
        document = Document(None, self.document_changed)
        document.open_file(file_path)
        self.editor.addTab(document, "")
        self.editor.setCurrentIndex(self.editor.count() - 1)
        self.set_tab_title()
        self.editor.currentWidget().text.setFocus()

    def set_tab_title(self):
        if (self.editor.currentWidget() is not None):
            file_path = self.editor.currentWidget().file_path
            if (file_path is not None):
                prefix = ""
                if (not self.editor.currentWidget().saved):
                    prefix = "* "
                self.editor.setTabText(
                    self.editor.currentIndex(),
                    prefix + self.editor.currentWidget().filename
                    )
                self.editor.setTabToolTip(
                    self.editor.currentIndex(),
                    file_path
                    )
            else:
                self.editor.setTabText(self.editor.currentIndex(), "*")

    def document_changed(self):
        if (self.editor.count()):
            self.editor.currentWidget().reload()
            self.set_tab_title()

#==============================================================================
class ColourButton(QtGui.QFrame):

    def __init__(self, parent, set_colour):
        super(ColourButton, self).__init__(parent)
        self.set_colour = set_colour
        self.colour = "#ff0000"
        
        self.colour_button = QtGui.QToolButton()
        self.colour_button.setToolTip(Configuration.TOOL_TIP["set_colour"])
        self.colour_button.setStatusTip(Configuration.TOOL_TIP["set_colour"])
        self.colour_button.clicked.connect(self.set_colour)
        self.colour_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["letter"])
            )

        dialog_button = QtGui.QToolButton()
        dialog_button.setToolTip(Configuration.TOOL_TIP["choose_colour"])
        dialog_button.setStatusTip(Configuration.TOOL_TIP["choose_colour"])
        dialog_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["down"])
            )
        dialog_button.clicked.connect(self.colour_dialog)
        dialog_button.setMaximumWidth(15)

        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(self.colour_button, 0, QtCore.Qt.AlignHCenter)
        layout.addWidget(dialog_button, 0, QtCore.Qt.AlignHCenter)
        layout.setContentsMargins(QtCore.QMargins(2,2,2,2))

        self.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Plain)
        self.update_ui()

    def update_ui(self):
        icon = self.colour_button.icon()
        style = "".join(
            [
                "background: ",
                self.colour
                ]
            )
        self.colour_button.setStyleSheet(style)

    def colour_dialog(self):
        colour = QtGui.QColorDialog.getColor()
        if (colour.isValid()):
            self.colour = str(colour.name())
            self.update_ui()
            self.set_colour(self.colour)
        
#==============================================================================
class FindDialog(QtGui.QDockWidget):

    def __init__(self, parent):
       super(FindDialog, self).__init__(
           Configuration.USER_TEXT["find_title"],
           parent
           )
       self.move(parent.frameGeometry().center())
       find_widget = FindWidget(parent.editor)
       self.setWidget(find_widget)
       self.topLevelChanged.connect(self.adjustSize)
       self.setFloating(True)
       self.show()

#==============================================================================
class FindWidget(QtGui.QWidget):

    def __init__(self, editor):
       super(FindWidget, self).__init__()
       
       self.editor = editor

       self.find_backwards = False
       self.find_case_sensitive = False
       self.find_whole_words = False
       
       self.initialise_ui()

    def initialise_ui(self):
       label = QtGui.QLabel(Configuration.USER_TEXT["find_what"])
       self.line_edit = QtGui.QLineEdit()
       self.line_edit.returnPressed.connect(self.find)
       label.setBuddy(self.line_edit)
       

       case_box = QtGui.QCheckBox(Configuration.USER_TEXT["match_case"])
       case_box.stateChanged.connect(self.find_case_changed)

       backward_box = QtGui.QCheckBox(
           Configuration.USER_TEXT["search_backwards"]
           )
       backward_box.stateChanged.connect(self.find_backwards_changed)

       whole_words_box = QtGui.QCheckBox(
           Configuration.USER_TEXT["match_whole_words"]
           )
       whole_words_box.stateChanged.connect(self.find_whole_words_changed)

       find_button = QtGui.QPushButton(
           Configuration.USER_TEXT["find"]
           )
       find_button.clicked.connect(self.find)

       close_button = QtGui.QPushButton(Configuration.USER_TEXT["close"])
       close_button.clicked.connect(self.close)

       top_left_layout = QtGui.QHBoxLayout()
       top_left_layout.addWidget(label)
       top_left_layout.addWidget(self.line_edit)

       left_layout = QtGui.QVBoxLayout()
       left_layout.addLayout(top_left_layout)
       left_layout.addWidget(case_box)
       left_layout.addWidget(backward_box)
       left_layout.addWidget(whole_words_box)
       left_layout.addStretch()

       right_layout = QtGui.QVBoxLayout()
       right_layout.addWidget(find_button)
       right_layout.addWidget(close_button)
       #right_layout.setAlignment(QtCore.Qt.AlignLeft)
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

    def find(self):
        if (self.editor.count()):
            text = self.line_edit.text()
            found = self.editor.currentWidget().text.find(
                text,
                self.get_find_flags()
                )
            if (found):
                self.editor.currentWidget().activateWindow()
                self.editor.currentWidget().text.setFocus()
            else:
                cant_find_dialog = QtGui.QMessageBox(
                    QtGui.QMessageBox.Information,
                    "Not Found",
                    "The following specified text was not found:",
                    QtGui.QMessageBox.Ok,
                    self
                    ) 
                cant_find_dialog.setInformativeText(text)
                cant_find_dialog.show()
        
#==============================================================================
class ConfigurationDialog(QtGui.QDialog):

   def __init__(self, parent):
       super(ConfigurationDialog, self).__init__(parent)

       self.config = copy.copy(Configuration.OPTIONS)

       main_layout = QtGui.QVBoxLayout()

       for key in self.config:
           layout = QtGui.QHBoxLayout()
           main_layout.addLayout(layout)

           value = self.config[key]
           if (isinstance(value, bool)):
               widget = QtGui.QCheckBox(key, self)
               if (value):
                   widget.setCheckState(QtCore.Qt.Checked)
               else:
                   widget.setCheckState(QtCore.Qt.Unchecked)
               def change_function(name):
                   return lambda state : self.bool_changed(name, state)
               widget.stateChanged.connect(change_function(key))
           layout.addWidget(widget)

       # add a save and a cancel button
       bottom_buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Save |  QtGui.QDialogButtonBox.Cancel
           )
       bottom_buttons.accepted.connect(self.save_and_close)
       bottom_buttons.rejected.connect(self.close)
       main_layout.addWidget(bottom_buttons)

       self.setLayout(main_layout)
       

       self.setWindowTitle(Configuration.USER_TEXT["configuration"])
       self.exec_()

   def save_and_close(self):
       for key in self.config:
           Configuration.OPTIONS[key] = self.config[key]
       self.close()

   def bool_changed(self, key, state):
       self.config[key] = bool(state)

#==============================================================================
class Document(QtGui.QWidget):

    def __init__(self, parent, callback):
        super(Document, self).__init__(parent)

        self.file_path = None
        self.saved = True

        self.text = QtGui.QTextEdit(self)
        self.text.textChanged.connect(callback)
        self.text.verticalScrollBar().valueChanged.connect(
            lambda value : self.sync_scrollbars()
            )

        self.output = QtGui.QTextEdit(self)
        self.output.setReadOnly(True)

        horizontal_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        horizontal_splitter.addWidget(self.text)
        horizontal_splitter.addWidget(self.output)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(horizontal_splitter)

    @property
    def filename(self):
        if (self.file_path is not None):
            return os.path.basename(str(self.file_path))

    def sync_scrollbars(self):
        max_text_scroll = self.text.verticalScrollBar().maximum()
        if (max_text_scroll):
            value = self.text.verticalScrollBar().value()
            percentage_scrolled = float(value) / max_text_scroll

            output_scroll = self.output.verticalScrollBar()
            max_out_scroll = output_scroll.maximum()
            output_scroll.setValue(int(max_out_scroll * percentage_scrolled))

    def check_saved(self):
        if (self.file_path is not None):
            with open(self.file_path, "r") as current_file:
                content = current_file.read()
            self.saved = self.text.toPlainText() == content

    def reload(self):
        html = self.convert_input()
        self.output.clear()
        if (Configuration.OPTIONS["Show html"]):
            self.output.insertPlainText(html)
        else:
            self.output.insertHtml(html)
        self.check_saved()
        self.sync_scrollbars()

    def convert_input(self):
        markdown_string = self.text.toPlainText()
        return markdown.markdown(str(markdown_string))

    def save_file(self):
        with open(self.file_path, "w") as text_file:
            filedata = self.text.toPlainText()
            text_file.write(filedata)
        self.saved = True

    def open_file(self, file_path):
        with open(file_path, "r") as read_file:
            filedata = read_file.read()
            self.text.setText(filedata)
        self.file_path = file_path
        self.reload()

    def export_html(self, file_path):
        html = self.convert_input()
        with open(file_path, "w") as html_file:
            html_file.write(html)

    def colour_highlighted(self, colour):
        self.edit_selection("<font color=\"" + colour + "\">", "</font>")

    def bold_highlighted(self):
        self.edit_selection("__", "__")

    def italic_highlighted(self):
        self.edit_selection("_", "_")

    def code_block_highlighted(self):
        self.edit_selection("```\n", "\n```")

    def upper(self):
        """ 
        If there is a selection it will make it upper case, otherwise it will 
        make the next word upper case.
        """
        cursor = self.text.textCursor()
        if (cursor.hasSelection()):
            print cursor.selectedText()

    def edit_selection(self, beginning, end, empty=False):
        """
        Do an edit to the current selection. Add beginning to the start and end
        to the end.
        
        if selection is empty variable empty controls if anything is added,
        """
        cursor = self.text.textCursor()
        if (cursor.hasSelection() or not empty):
            text = cursor.selectedText()
            text.prepend(beginning)
            text.append(end)
            cursor.insertText(text)

#==============================================================================
def process_markdown(markdown_string):
    return markdown.markdown(markdown_string, ["extra"])

#==============================================================================
def main():
    app = QtGui.QApplication(sys.argv)
    editor = MarkdownEditor(sys.argv[1:])
    sys.exit(app.exec_())

#==============================================================================
if (__name__ == "__main__"):
    main()
