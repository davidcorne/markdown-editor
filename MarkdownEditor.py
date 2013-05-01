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
class MarkdownEditor(QtGui.QMainWindow):
 
    def __init__(self):
        super(MarkdownEditor, self).__init__()
        self.initialise_UI()
        self.config = DEFAULT_CONFIG
        self.editor = QtGui.QTabWidget(self)
        self.setCentralWidget(self.editor)
         
    def initialise_UI(self):
        self.create_menu()
        self.create_toolbars()
        self.setWindowTitle("MarkdownEditor")
        self.resize(1200, 600)
        self.centre()
        self.show()

    def centre(self):
        """ Centre the window in the screen. """
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_toolbars(self):
        self.create_standard_toolbar()

    def create_standard_toolbar(self):
        standard_toolbar = QtGui.QToolBar("Standard Toolbar")
        style = QtGui.QApplication.style()
        
        # add the buttons
        new_button = QtGui.QToolButton()
        new_button.setIcon(
            style.standardIcon(style.SP_FileIcon)
            )
        new_button.setToolTip("Create new file")
        new_button.clicked.connect(self.new_file)
        standard_toolbar.addWidget(new_button)

        save_button = QtGui.QToolButton()
        save_button.setIcon(
            style.standardIcon(style.SP_DriveFDIcon)
            )
        save_button.setToolTip("Save current file")
        save_button.clicked.connect(self.save_file)
        standard_toolbar.addWidget(save_button)

        open_button = QtGui.QToolButton()
        open_button.setIcon(
            style.standardIcon(style.SP_FileIcon)
            )
        open_button.setToolTip("Open file")
        open_button.clicked.connect(self.open_file)
        standard_toolbar.addWidget(open_button)

        save_as_button = QtGui.QToolButton()
        save_as_button.setIcon(
            style.standardIcon(style.SP_DriveFDIcon)
            )
        save_as_button.setToolTip("Write current document to file")
        save_as_button.clicked.connect(self.save_file_as)
        standard_toolbar.addWidget(save_as_button)

        # now change the standard toolbar properties
        standard_toolbar.setMovable(True)
        standard_toolbar.setFloatable(True)
        standard_toolbar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.addToolBar(standard_toolbar)

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
        open_action.triggered.connect(self.open_file)
         
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

    def new_file(self):
        document = Document(None, self.config, self.document_changed)
        self.editor.addTab(document, "")
        self.editor.setCurrentIndex(self.editor.count() - 1)
        self.set_tab_title()
         
    def export_html(self):
        if (self.editor.count() != 0):
            filename = QtGui.QFileDialog.getSaveFileName(
                self,
                "Export HTML",
                ".",
                "HTML (*.html)"
                )
            if (filename):
                self.editor.currentWidget().export_html(filename)

    def close_file(self):
        if (self.editor.count() == 0):
            # there is no tab, so close the program
            self.close()
        else:
            #if (not self.editor.currentWidget().saved):
            #    # have a dialog here for saving current tab
            #    pass
            self.editor.removeTab(self.editor.currentIndex())
         
    def save_file_as(self):
        if (self.editor.count() != 0):
            filename = QtGui.QFileDialog.getSaveFileName(
                self,
                "Save File",
                ".",
                MARKDOWN_FILE_STRING
                )
            if (filename):
                self.editor.currentWidget().filename = filename
                self.editor.currentWidget().save_file()
                self.set_tab_title()

    def save_file(self):
        if (self.editor.count() != 0):
            if (self.editor.currentWidget().filename):
                self.editor.currentWidget().save_file()
            else:
                self.save_file_as()
         
    def open_file(self):
        filename = QtGui.QFileDialog.getOpenFileName(
            self,
            "Open File",
            ".",
            MARKDOWN_FILE_STRING
            )
        if (filename):
            document = Document(None, self.config, self.document_changed)
            document.open_file(filename)
            self.editor.addTab(document, "")
            self.editor.setCurrentIndex(self.editor.count() - 1)
            self.set_tab_title()

    def set_tab_title(self):
        if (self.editor.currentWidget() is not None):
            filename = self.editor.currentWidget().filename
            if (filename is not None):
                self.editor.setTabText(
                    self.editor.currentIndex(),
                    os.path.basename(str(filename))
                    )
                self.editor.setTabToolTip(
                    self.editor.currentIndex(),
                    filename
                    )
            else:
                self.editor.setTabText(self.editor.currentIndex(), "*")

    def document_changed(self):
        self.set_tab_title()

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
                   return lambda state:  self.bool_changed(name, state)
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

        self.text = QtGui.QTextEdit(self)
        self.text.textChanged.connect(self.on_text_changed)
        self.text.verticalScrollBar().valueChanged.connect(self.text_scrolled)

        self.output = QtGui.QTextEdit(self)
        self.output.setReadOnly(True)

        horizontal_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        horizontal_splitter.addWidget(self.text)
        horizontal_splitter.addWidget(self.output)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(horizontal_splitter)
        
        self.config = config
        self.callback = callback

        self.filename = None
    
    def text_scrolled(self, value):
        max_text_scroll = self.text.verticalScrollBar().maximum()
        percentage_scrolled = float(value) / max_text_scroll
        
        output_scroll = self.output.verticalScrollBar()
        max_out_scroll = output_scroll.maximum()
        output_scroll.setValue(int(max_out_scroll * percentage_scrolled))

    def on_text_changed(self):
        self.reload()
        self.callback()

    def reload(self):
        html = self.convert_input()
        self.output.clear()
        if (self.config["Debug"]):
            self.output.insertPlainText(html)
        else:
            self.output.insertHtml(html)

    def convert_input(self):
        markdown_string = self.text.toPlainText()
        return markdown.markdown(str(markdown_string))
        
    def save_file(self):
        assert self.filename is not None
        with open(self.filename, "w") as text_file:
            filedata = self.text.toPlainText()
            text_file.write(filedata)

    def open_file(self, filename):
        with open(filename, "r") as read_file:
            filedata = read_file.read()
            self.text.setText(filedata)
        self.filename = filename

    def export_html(self, filename):
        assert self.filename is not None
        html = self.convert_input()
        with open(filename, "w") as html_file:
            html_file.write(html)
        
def process_markdown(markdown_string):
    return markdown.markdown(markdown_string, ["extra"])

#==============================================================================
def main():
    app = QtGui.QApplication(sys.argv)
    editor = MarkdownEditor()
    sys.exit(app.exec_())
     
#==============================================================================
if (__name__ == "__main__"):
    main()
