#! /usr/bin/python

import copy
import sys
import os
import markdown

from PyQt4 import QtGui, QtCore

MARKDOWN_FILE_STRING = """\
Markdown (*.md *.markdown *.mdown *.mkdn *.mkd *.mdtxt *.mdtext *.text);;\
All Files (*)\
"""

DEFAULT_CONFIG = {
    "Debug": False,
    }

#==============================================================================
def find_images():
    images = dict()
    directory = "Images"
    for image in os.listdir(directory):
        images[os.path.splitext(image)[0]] = os.path.join(directory, image)
    return images

#==============================================================================
class MarkdownEditor(QtGui.QMainWindow):

    def __init__(self, files):
        """
        files is an iterable of files to open.
        """
        super(MarkdownEditor, self).__init__()
        self.images = find_images()
        self.config = DEFAULT_CONFIG
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
        self.setWindowTitle("MarkdownEditor")
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
        self.create_format_toolbar()

    def create_format_toolbar(self):
        format_toolbar = QtGui.QToolBar("Format Toolbar")

        bold_button = QtGui.QToolButton()
        bold_button.setIcon(
            QtGui.QIcon(self.images["bold"])
            )
        bold_button.setToolTip(
            "Surround the highlighted area with strong emphasis (__)"
            )
        bold_button.clicked.connect(self.bold_highlighted)

        italic_button = QtGui.QToolButton()
        italic_button.setIcon(
            QtGui.QIcon(self.images["italic"])
            )
        italic_button.setToolTip(
            "Surround the highlighted area with emphasis (_)"
            )
        italic_button.clicked.connect(self.italic_highlighted)

        code_button = QtGui.QToolButton()
        code_button.setIcon(
            QtGui.QIcon(self.images["code"])
            )
        code_button.setToolTip(
            "Surround the highlighted area with code blocks (```)"
            )
        code_button.clicked.connect(self.code_highlighted)

        colour_button = ColourButton(self, self.colour_highlighted, self.images)

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
        file_toolbar = QtGui.QToolBar("File Toolbar")

        # add the buttons
        new_button = QtGui.QToolButton()
        new_button.setIcon(
            QtGui.QIcon(self.images["new_file"])
            )
        new_button.setToolTip("Create new file")
        new_button.clicked.connect(self.new_file)

        save_button = QtGui.QToolButton()
        save_button.setIcon(
            QtGui.QIcon(self.images["save_file"])
            )
        save_button.setToolTip("Save current file")
        save_button.clicked.connect(self.save_file)

        open_button = QtGui.QToolButton()
        open_button.setIcon(
            QtGui.QIcon(self.images["open_file"])
            )
        open_button.setToolTip("Open file")
        open_button.clicked.connect(self.query_open_file)

        save_all_button = QtGui.QToolButton()
        save_all_button.setIcon(
            QtGui.QIcon(self.images["save_all"])
            )
        save_all_button.setToolTip("Write all current documents to file")
        save_all_button.clicked.connect(self.save_all_files)

        export_html_button = QtGui.QToolButton()
        export_html_button.setIcon(
            QtGui.QIcon(self.images["export_html"])
            )
        export_html_button.setToolTip("Export html output to file")
        export_html_button.clicked.connect(self.export_html)

        file_toolbar.addWidget(new_button)
        file_toolbar.addWidget(open_button)
        file_toolbar.addWidget(save_button)
        file_toolbar.addWidget(save_all_button)
        file_toolbar.addWidget(export_html_button)

        # now change the file toolbar properties
        file_toolbar.setMovable(True)
        file_toolbar.setFloatable(True)
        file_toolbar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.addToolBar(file_toolbar)

    def create_edit_toolbar(self):
        edit_toolbar = QtGui.QToolBar("Edit Toolbar")

        # add the buttons
        cut_button = QtGui.QToolButton()
        cut_button.setIcon(
            QtGui.QIcon(self.images["cut"])
            )
        cut_button.setToolTip("")
        cut_button.clicked.connect(self.cut)

        copy_button = QtGui.QToolButton()
        copy_button.setIcon(
            QtGui.QIcon(self.images["copy"])
            )
        copy_button.setToolTip("")
        copy_button.clicked.connect(self.copy)

        paste_button = QtGui.QToolButton()
        paste_button.setIcon(
            QtGui.QIcon(self.images["paste"])
            )
        paste_button.setToolTip("")
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
        self.create_tools_menu()

    def create_tools_menu(self):
        configure_action = QtGui.QAction("Configure", self)
        configure_action.setStatusTip("Configure MarkdownEditor")
        configure_action.triggered.connect(self.raise_configure_dialog)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&Tools")
        file_menu.addAction(configure_action)

    def create_file_menu(self):
        new_action = QtGui.QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.setStatusTip("Create new file")
        new_action.triggered.connect(self.new_file)

        save_action = QtGui.QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip("Save current file")
        save_action.triggered.connect(self.save_file)

        save_as_action = QtGui.QAction("Save As", self)
        save_as_action.setShortcut("F12")
        save_as_action.setStatusTip("Write current document to file")
        save_as_action.triggered.connect(self.save_file_as)

        open_action = QtGui.QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Open a file")
        open_action.triggered.connect(self.query_open_file)

        close_action = QtGui.QAction("Close", self)
        close_action.setShortcut("Ctrl+F4")
        close_action.setStatusTip("Close MarkdownEditor")
        close_action.triggered.connect(self.close_file)

        export_action = QtGui.QAction("Export HTML", self)
        export_action.setStatusTip("Export as HTML")
        export_action.triggered.connect(self.export_html)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(export_action)

    def raise_configure_dialog(self):
        config_dialog = ConfigurationDialog(self, self.config)
        self.editor.currentWidget().reload()

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

    def new_file(self):
        document = Document(None, self.config, self.document_changed)
        self.editor.addTab(document, "")
        self.editor.setCurrentIndex(self.editor.count() - 1)
        self.set_tab_title()

    def export_html(self):
        if (self.editor.count() != 0):
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
        if (self.editor.count() != 0):
            file_path = QtGui.QFileDialog.getSaveFileName(
                "THING",
                self,
                "Save File",
                ".",
                MARKDOWN_FILE_STRING
                )
            if (file_path):
                self.editor.currentWidget().file_path = file_path
                self.editor.currentWidget().save_file()
                self.set_tab_title()

    def save_file(self):
        if (self.editor.count() != 0):
            if (self.editor.currentWidget().file_path):
                self.editor.currentWidget().save_file()
            else:
                self.save_file_as()
            self.set_tab_title()

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
            MARKDOWN_FILE_STRING
            )
        if (file_path):
            self.open_file(file_path)

    def open_file(self, file_path):
        document = Document(None, self.config, self.document_changed)
        document.open_file(file_path)
        self.editor.addTab(document, "")
        self.editor.setCurrentIndex(self.editor.count() - 1)
        self.set_tab_title()

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
        self.set_tab_title()

#==============================================================================
class ColourButton(QtGui.QFrame):

    def __init__(self, parent, callback, images):
        super(ColourButton, self).__init__(parent)
        self.callback = callback
        self.colour = "#000000"
        
        self.colour_button = QtGui.QToolButton()
        self.colour_button.setToolTip("Change colour of highlighted text")
        self.colour_button.clicked.connect(self.set_colour)
        #self.colour_button.setMaximumHeight(11)
        self.colour_button.setContentsMargins(QtCore.QMargins(0,0,0,0))

        dialog_button = QtGui.QToolButton()
        dialog_button.setToolTip("Pick colour to change text to")
        dialog_button.setIcon(
            QtGui.QIcon(images["down"])
            )
        dialog_button.clicked.connect(self.colour_dialog)
        dialog_button.setMaximumWidth(11)
        dialog_button.setContentsMargins(QtCore.QMargins(0,0,0,0))

        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(self.colour_button, 0, QtCore.Qt.AlignHCenter)
        layout.addWidget(dialog_button, 0, QtCore.Qt.AlignHCenter)
        layout.setContentsMargins(QtCore.QMargins(2,2,2,2))

        self.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Plain)
        self.update_ui()

    def update_ui(self):
        self.colour_button.setStyleSheet("background-color: " + self.colour)

    def set_colour(self):
        self.callback(self.colour)

    def colour_dialog(self):
        colour = QtGui.QColorDialog.getColor()
        if (colour.isValid()):
            self.colour = str(colour.name())
            self.update_ui()
            self.set_colour()
        
#==============================================================================
class ConfigurationDialog(QtGui.QDialog):

   def __init__(self, parent, configuration):
       super(ConfigurationDialog, self).__init__(parent)

       self.parent_config = configuration
       self.config = copy.copy(configuration)

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
       bottom_button_layout = QtGui.QHBoxLayout()

       save_button = QtGui.QPushButton("Save & Close", self)
       save_button.clicked.connect(self.save_and_close)
       bottom_button_layout.addWidget(save_button)

       cancel_button = QtGui.QPushButton("Cancel", self)
       cancel_button.clicked.connect(self.close)
       bottom_button_layout.addWidget(cancel_button)

       main_layout.addLayout(bottom_button_layout)

       self.setLayout(main_layout)

       self.setWindowTitle("Configuration")
       self.exec_()

   def save_and_close(self):
       for key in self.config:
           self.parent_config[key] = self.config[key]
       self.close()

   def bool_changed(self, key, state):
       self.config[key] = bool(state)

#==============================================================================
class Document(QtGui.QWidget):

    def __init__(self, parent, config, callback):
        super(Document, self).__init__(parent)

        self.file_path = None
        self.saved = True
        self.config = config
        self.callback = callback

        self.text = QtGui.QTextEdit(self)
        self.text.textChanged.connect(self.on_text_changed)
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
        if (max_text_scroll != 0):
            value = self.text.verticalScrollBar().value()
            percentage_scrolled = float(value) / max_text_scroll

            output_scroll = self.output.verticalScrollBar()
            max_out_scroll = output_scroll.maximum()
            output_scroll.setValue(int(max_out_scroll * percentage_scrolled))

    def on_text_changed(self):
        self.reload()
        self.callback()

    def check_saved(self):
        if (self.file_path is not None):
            with open(self.file_path, "r") as current_file:
                content = current_file.read()
            self.saved = self.text.toPlainText() == content

    def reload(self):
        html = self.convert_input()
        self.output.clear()
        if (self.config["Debug"]):
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
