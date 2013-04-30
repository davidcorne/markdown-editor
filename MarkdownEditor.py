#! /usr/bin/python
 
import sys
import os
import markdown

from PyQt4 import QtGui, QtCore
 
MARKDOWN_FILE_STRING = """\
Markdown (*.md *.markdown *.mdown *.mkdn *.mkd *.mdtxt *.mdtext *.text);;\
All Files (*)\
"""

#==============================================================================
class MarkdownEditor(QtGui.QMainWindow):
 
    def __init__(self):
        super(MarkdownEditor, self).__init__()
        self.initialise_UI()
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
         
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
         
    def new_file(self):
        document = Document(None)
        self.editor.addTab(document, "")
        self.editor.setCurrentIndex(self.editor.count() - 1)
        self.set_tab_title()
         
    def close_file(self):
        if (self.editor.count() == 0):
            # there is no tab, so close the program
            self.close()
        else:
            if (not self.editor.currentWidget().saved):
                # have a dialog here for saving current tab
                pass
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
            document = Document(None)
            document.open_file(filename)
            self.editor.addTab(document, "")
            self.editor.setCurrentIndex(self.editor.count() - 1)
            self.set_tab_title()

    def set_tab_title(self):
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

#==============================================================================
class Document(QtGui.QWidget):
    
    def __init__(self, parent):
        super(Document, self).__init__(parent)

        self.text = QtGui.QTextEdit(self)
        self.text.textChanged.connect(self.on_text_changed)

        self.output = QtGui.QTextEdit(self)
        self.output.setReadOnly(True)

        horizontal_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        horizontal_splitter.addWidget(self.text)
        horizontal_splitter.addWidget(self.output)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(horizontal_splitter)
        
        self.filename = None
        self.saved = True
    
    def on_text_changed(self):
        markdown_string = self.text.toPlainText()
        html = markdown.markdown(str(markdown_string))
        self.output.clear()
        self.output.insertHtml(html)
        self.saved = False
         
    def save_file(self):
        assert self.filename is not None
        with open(self.filename, "w") as text_file:
            filedata = self.text.toPlainText()
            text_file.write(filedata)
        self.saved = True

    def open_file(self, filename):
        with open(filename, "r") as read_file:
            filedata = read_file.read()
            self.text.setText(filedata)
        self.filename = filename

def process_markdown(markdown_string):
    return markdown.markdown(markdown_string)

#==============================================================================
def main():
    app = QtGui.QApplication(sys.argv)
    editor = MarkdownEditor()
    sys.exit(app.exec_())
     
#==============================================================================
if (__name__ == "__main__"):
    main()
