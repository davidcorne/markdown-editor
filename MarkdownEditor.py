#! /usr/bin/python

# python imports

from __future__ import unicode_literals

import cgi
import os
import time

from PyQt4 import QtGui, QtCore, QtWebKit

# local imports

import Configuration
import ConfigurationDialog
import Error
import Examples

from UserText import USER_TEXT
from ToolTips import TOOL_TIP

#==============================================================================
class MarkdownEditorApp(QtGui.QApplication):

    def __init__(self, command_args):
        super(MarkdownEditorApp, self).__init__(command_args)
        self.setWindowIcon(QtGui.QIcon(Configuration.IMAGES["icon"]))

#==============================================================================
class DocumentTabBar(QtGui.QTabBar):
    
    def __init__(self):
        super(DocumentTabBar, self).__init__()
        self.setTabsClosable(True)
        self.setMovable(True)

    def mouseReleaseEvent(self, event):
        if (event.button() == QtCore.Qt.MidButton):
            self.tabCloseRequested.emit(self.tabAt(event.pos()))
        super(DocumentTabBar, self).mouseReleaseEvent(event)

#==============================================================================
class DocumentTabs(QtGui.QTabWidget):

    def __init__(self, parent, tab_close_function):
        super(DocumentTabs, self).__init__(parent)
        self.tabCloseRequested.connect(tab_close_function)
        self.setTabBar(DocumentTabBar())
        next_child_shortcut = QtGui.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.NextChild),
            self
            )
        next_child_shortcut.activated.connect(self.next_child)

        previous_child_shortcut = QtGui.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.PreviousChild),
            self
            )
        previous_child_shortcut.activated.connect(self.previous_child)

    def next_child(self):
        new_index = (self.currentIndex() + 1) % self.count()
        self.setCurrentIndex(new_index)        
        
    def previous_child(self):
        new_index = (self.currentIndex() - 1) % self.count()
        self.setCurrentIndex(new_index)        
        
#==============================================================================
class MarkdownEditor(QtGui.QMainWindow):

    def __init__(self, files):
        """
        files is an iterable of files to open.
        """
        super(MarkdownEditor, self).__init__()
        
        self.editor = DocumentTabs(self, self.tab_close_requested)
        self.initialise_UI()
        self.setCentralWidget(self.editor)
        
        for markdown in files:
            try:
                self.open_file(markdown)
            except IOError:
                Error.show_error(USER_TEXT["file_not_found"] %(markdown))

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
        
        self.setWindowTitle(USER_TEXT["program_name"])
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
        frame = self.frameGeometry()
        screen_centre = QtGui.QDesktopWidget().availableGeometry().center()
        frame.moveCenter(screen_centre)
        self.move(frame.topLeft())

    def create_toolbars(self):
        self.create_file_toolbar()
        self.create_edit_toolbar()
        self.create_undo_redo_toolbar()
        self.create_format_toolbar()

    def create_undo_redo_toolbar(self):
        undo_redo_toolbar = QtGui.QToolBar(
            USER_TEXT["undo_redo_toolbar"]
            )

        undo_button = QtGui.QToolButton()
        undo_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["undo"])
            )
        undo_button.setToolTip(TOOL_TIP["undo"])
        undo_button.setStatusTip(TOOL_TIP["undo"])
        undo_button.clicked.connect(self.undo)

        redo_button = QtGui.QToolButton()
        redo_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["redo"])
            )
        redo_button.setToolTip(TOOL_TIP["redo"])
        redo_button.setStatusTip(TOOL_TIP["redo"])
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
            USER_TEXT["format_toolbar"]
            )

        bold_button = QtGui.QToolButton()
        bold_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["bold"])
            )
        bold_button.setToolTip(TOOL_TIP["bold"])
        bold_button.setStatusTip(TOOL_TIP["bold"])
        bold_button.setShortcut("Ctrl+B")
        bold_button.clicked.connect(self.bold_highlighted)

        italic_button = QtGui.QToolButton()
        italic_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["italic"])
            )
        italic_button.setToolTip(TOOL_TIP["italic"])
        italic_button.setStatusTip(TOOL_TIP["italic"])
        italic_button.setShortcut("Ctrl+I")
        italic_button.clicked.connect(self.italic_highlighted)

        code_button = QtGui.QToolButton()
        code_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["code"])
            )
        code_button.setToolTip(TOOL_TIP["code"])
        code_button.setStatusTip(TOOL_TIP["code"])
        code_button.setShortcut("Ctrl+Shift+C")
        code_button.clicked.connect(self.code_highlighted)

        link_button = QtGui.QToolButton()
        link_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["link"])
            )
        link_button.setToolTip(TOOL_TIP["link"])
        link_button.setStatusTip(TOOL_TIP["link"])
        link_button.setShortcut("Ctrl+L")
        link_button.clicked.connect(self.insert_link)

        image_button = QtGui.QToolButton()
        image_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["image"])
            )
        image_button.setToolTip(TOOL_TIP["image_menu"])
        image_button.setStatusTip(TOOL_TIP["image_menu"])
        image_button.setShortcut("Ctrl+M")
        image_button.setMenu(self.image_menu())
        image_button.setPopupMode(QtGui.QToolButton.InstantPopup)

        colour_button = ColourButton(self, self.colour_highlighted)

        format_toolbar.addWidget(bold_button)
        format_toolbar.addWidget(italic_button)
        format_toolbar.addWidget(code_button)
        format_toolbar.addWidget(link_button)
        format_toolbar.addWidget(image_button)
        format_toolbar.addWidget(colour_button)

        # now change the format toolbar properties
        format_toolbar.setMovable(True)
        format_toolbar.setFloatable(True)
        format_toolbar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.addToolBar(format_toolbar)

    def image_menu(self):
        """
        Returns a QMenu with options for linking images or embedding images.
        """
        menu = QtGui.QMenu()

        link_image = menu.addAction(USER_TEXT["link_image"])
        link_image.setIcon(QtGui.QIcon(Configuration.IMAGES["link"]))
        link_image.setStatusTip(TOOL_TIP["link_image"])
        link_image.setToolTip(TOOL_TIP["link_image"])
        link_image.triggered.connect(self.link_image)
        return menu

    def print_menu(self):
        """
        Returns a QMenu with all the print options.
        """
        menu = QtGui.QMenu()

        print_rendered_html = menu.addAction(
                USER_TEXT["print_rendered_html"]
                )
        print_rendered_html.setIcon(QtGui.QIcon(Configuration.IMAGES["print"]))
        print_rendered_html.setStatusTip(
            TOOL_TIP["print_rendered_html"]
            )
        print_rendered_html.triggered.connect(self.print_rendered_html_dialog)

        print_preview_rendered_html = menu.addAction(
                USER_TEXT["print_preview_rendered_html"]
                )
        print_preview_rendered_html.setIcon(
            QtGui.QIcon(Configuration.IMAGES["print_preview"])
            )
        print_preview_rendered_html.setStatusTip(
            TOOL_TIP["print_preview_rendered_html"]
            )
        print_preview_rendered_html.triggered.connect(
            self.print_preview_rendered_html
            )
        menu.addSeparator()
        
        print_markdown = menu.addAction(
            USER_TEXT["print_markdown"]
            )
        print_markdown.setIcon(QtGui.QIcon(Configuration.IMAGES["print"]))
        print_markdown.setStatusTip(TOOL_TIP["print_markdown"])
        print_markdown.triggered.connect(self.print_markdown_dialog)
        
        print_preview_markdown = menu.addAction(
                USER_TEXT["print_preview_markdown"]
                )
        print_preview_markdown.setIcon(
            QtGui.QIcon(Configuration.IMAGES["print_preview"])
            )
        print_preview_markdown.setStatusTip(
            TOOL_TIP["print_preview_markdown"]
            )
        print_preview_markdown.triggered.connect(self.print_preview_markdown)
        menu.addSeparator()

        print_raw_html = menu.addAction(
                USER_TEXT["print_raw_html"]
                )
        print_raw_html.setIcon(QtGui.QIcon(Configuration.IMAGES["print"]))
        print_raw_html.setStatusTip(TOOL_TIP["print_raw_html"])
        print_raw_html.triggered.connect(self.print_raw_html_dialog)

        print_preview_raw_html = menu.addAction(
                USER_TEXT["print_preview_raw_html"]
                )
        print_preview_raw_html.setIcon(
            QtGui.QIcon(Configuration.IMAGES["print_preview"])
            )
        print_preview_raw_html.setStatusTip(
            TOOL_TIP["print_preview_raw_html"]
            )
        print_preview_raw_html.triggered.connect(
            self.print_preview_raw_html
            )
        return menu

    def create_file_toolbar(self):
        file_toolbar = QtGui.QToolBar(
            USER_TEXT["file_toolbar"]
            )
        file_actions = [
            self.file_actions(),
            self.save_actions(), 
            self.output_actions()
            ]
        for actions in file_actions:
            for action in actions:
                button = QtGui.QToolButton()
                button.setDefaultAction(action)
                # this makes the buttons which are menus work correctly and 
                # doesn't break the ones without menus
                button.setPopupMode(QtGui.QToolButton.InstantPopup)
                file_toolbar.addWidget(button)

        # now change the file toolbar properties
        file_toolbar.setMovable(True)
        file_toolbar.setFloatable(True)
        file_toolbar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
        self.addToolBar(file_toolbar)

    def create_edit_toolbar(self):
        edit_toolbar = QtGui.QToolBar(
            USER_TEXT["edit_toolbar"]
            )

        # add the buttons
        cut_button = QtGui.QToolButton()
        cut_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["cut"])
            )
        cut_button.setToolTip(TOOL_TIP["cut"])
        cut_button.setStatusTip(TOOL_TIP["cut"])
        cut_button.clicked.connect(self.cut)

        copy_button = QtGui.QToolButton()
        copy_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["copy"])
            )
        copy_button.setToolTip(TOOL_TIP["copy"])
        copy_button.setStatusTip(TOOL_TIP["copy"])
        copy_button.clicked.connect(self.copy)

        paste_button = QtGui.QToolButton()
        paste_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["paste"])
            )
        paste_button.setToolTip(TOOL_TIP["paste"])
        paste_button.setStatusTip(TOOL_TIP["paste"])
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
        self.create_help_menu()

    def create_help_menu(self):
        # make help a member so it sticks around, also doesn't override built 
        # in help
        self.help = Help()
        
        markdown_action = QtGui.QAction(
            USER_TEXT["markdown"], 
            self
            )
        markdown_action.setIcon(QtGui.QIcon(Configuration.IMAGES["markdown"]))
        markdown_action.setStatusTip(TOOL_TIP["help_link"])
        markdown_action.triggered.connect(self.help.markdown_description)

        markdown_extra_action = QtGui.QAction(
            USER_TEXT["markdown_extra"],
            self
            )
        markdown_extra_action.setIcon(
            QtGui.QIcon(Configuration.IMAGES["markdown"])
            )
        markdown_extra_action.setStatusTip(TOOL_TIP["help_link"])
        markdown_extra_action.triggered.connect(
            self.help.markdown_extra_description
            )

        markdown_all_action = QtGui.QAction(
            USER_TEXT["markdown_all"],
            self
            )
        markdown_all_action.setIcon(
            QtGui.QIcon(Configuration.IMAGES["markdown"])
            )
        markdown_all_action.setStatusTip(TOOL_TIP["help_link"])
        markdown_all_action.triggered.connect(
            self.help.markdown_all_description
            )

        codehilite_action = QtGui.QAction(
            USER_TEXT["codehilite"], 
            self
            )
        codehilite_action.setIcon(
            QtGui.QIcon(Configuration.IMAGES["markdown"])
            )
        codehilite_action.setStatusTip(TOOL_TIP["help_link"])
        codehilite_action.triggered.connect(self.help.codehilite_description)

        github_flavour_action = QtGui.QAction(
            USER_TEXT["github_flavoured_markdown"], 
            self
            )
        github_flavour_action.setIcon(
            QtGui.QIcon(Configuration.IMAGES["markdown"])
            )
        github_flavour_action.setStatusTip(TOOL_TIP["help_link"])
        github_flavour_action.triggered.connect(self.help.github_description)

        link_action = QtGui.QAction(USER_TEXT["help_link"], self)
        link_action.setStatusTip(TOOL_TIP["help_link"])
        link_action.triggered.connect(self.help.open_link)

        menu_bar = self.menuBar()
        help_menu = menu_bar.addMenu(USER_TEXT["help_menu"])
        help_menu.addAction(markdown_action)
        help_menu.addAction(markdown_extra_action)
        help_menu.addAction(markdown_all_action)
        help_menu.addAction(codehilite_action)
        help_menu.addAction(github_flavour_action)
        help_menu.addSeparator()
        help_menu.addAction(link_action)

    def create_edit_menu(self):
        undo_action = QtGui.QAction(USER_TEXT["undo"], self)
        undo_action.setIcon(QtGui.QIcon(Configuration.IMAGES["undo"]))
        undo_action.setStatusTip(TOOL_TIP["undo"])
        undo_action.triggered.connect(self.undo)

        redo_action = QtGui.QAction(USER_TEXT["redo"], self)
        redo_action.setIcon(QtGui.QIcon(Configuration.IMAGES["redo"]))
        redo_action.setStatusTip(TOOL_TIP["redo"])
        redo_action.triggered.connect(self.redo)

        cut_action = QtGui.QAction(USER_TEXT["cut"], self)
        cut_action.setIcon(QtGui.QIcon(Configuration.IMAGES["cut"]))
        cut_action.setStatusTip(TOOL_TIP["cut"])
        cut_action.triggered.connect(self.cut)

        copy_action = QtGui.QAction(USER_TEXT["copy"], self)
        copy_action.setIcon(QtGui.QIcon(Configuration.IMAGES["copy"]))
        copy_action.setStatusTip(TOOL_TIP["copy"])
        copy_action.triggered.connect(self.copy)

        paste_action = QtGui.QAction(USER_TEXT["paste"], self)
        paste_action.setIcon(QtGui.QIcon(Configuration.IMAGES["paste"]))
        paste_action.setStatusTip(TOOL_TIP["paste"])
        paste_action.triggered.connect(self.paste)

        select_all_action = QtGui.QAction(
            USER_TEXT["select_all"],
            self
            )
        select_all_action.setStatusTip(TOOL_TIP["select_all"])
        select_all_action.triggered.connect(self.select_all)

        search_action = QtGui.QAction(
            USER_TEXT["find_and_replace"], 
            self
            )
        search_action.setIcon(QtGui.QIcon(Configuration.IMAGES["find"]))
        search_action.setShortcut("Ctrl+F")
        search_action.setStatusTip(TOOL_TIP["find_and_replace"])
        search_action.triggered.connect(self.raise_find_dialog)

        menu_bar = self.menuBar()
        edit_menu = menu_bar.addMenu(USER_TEXT["edit_menu"])
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
            USER_TEXT["options"], 
            self
            )
        configure_action.setIcon(
            QtGui.QIcon(Configuration.IMAGES["configure"])
            )
        configure_action.setStatusTip(TOOL_TIP["configure"])
        configure_action.triggered.connect(self.raise_configure_dialog)

        menu_bar = self.menuBar()
        tools_menu = menu_bar.addMenu(USER_TEXT["tools_menu"])
        tools_menu.addAction(configure_action)

    def create_file_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu(USER_TEXT["file_menu"])
        file_actions = [
            self.file_actions(),
            self.save_actions(),
            self.output_actions()
            ]
        for actions in file_actions:
            for action in actions:
                file_menu.addAction(action)
            file_menu.addSeparator()

    def file_actions(self):
        new_action = QtGui.QAction(USER_TEXT["new_file"], self)
        new_action.setIcon(QtGui.QIcon(Configuration.IMAGES["new_file"]))
        new_action.setShortcut("Ctrl+N")
        new_action.setStatusTip(TOOL_TIP["new_file"])
        new_action.setToolTip(TOOL_TIP["new_file"])
        new_action.triggered.connect(self.new_file)

        open_action = QtGui.QAction(USER_TEXT["open_file"], self)
        open_action.setIcon(QtGui.QIcon(Configuration.IMAGES["open_file"]))
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip(TOOL_TIP["open_file"])
        open_action.setToolTip(TOOL_TIP["open_file"])
        open_action.triggered.connect(self.query_open_file)

        close_action = QtGui.QAction(
            USER_TEXT["close_file"],
            self
            )
        close_action.setIcon(QtGui.QIcon(Configuration.IMAGES["close_file"]))
        close_action.setShortcut("Ctrl+F4")
        close_action.setStatusTip(TOOL_TIP["close_file"])
        close_action.setToolTip(TOOL_TIP["close_file"])
        close_action.triggered.connect(self.close_file)

        # only make each action once, otherwise shortcuts are ambiguous
        if (not hasattr(self, "_file_actions")):
            self._file_actions = list()
            self._file_actions.append(new_action)
            self._file_actions.append(open_action)
            self._file_actions.append(close_action)

        return self._file_actions

    def save_actions(self):
        save_action = QtGui.QAction(USER_TEXT["save_file"], self)
        save_action.setIcon(QtGui.QIcon(Configuration.IMAGES["save_file"]))
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip(TOOL_TIP["save_file"])
        save_action.setToolTip(TOOL_TIP["save_file"])
        save_action.triggered.connect(self.save_file)

        save_as_action = QtGui.QAction(
            USER_TEXT["save_as"],
            self
            )
        save_as_action.setIcon(QtGui.QIcon(Configuration.IMAGES["save_as"]))
        save_as_action.setShortcut("F12")
        save_as_action.setStatusTip(TOOL_TIP["save_as"])
        save_as_action.setToolTip(TOOL_TIP["save_as"])
        save_as_action.triggered.connect(self.save_file_as)

        save_all_action =  QtGui.QAction(
            USER_TEXT["save_all"],
            self
            )
        save_all_action.setIcon(QtGui.QIcon(Configuration.IMAGES["save_all"]))
        save_all_action.setShortcut("Ctrl+Shift+S")
        save_all_action.setStatusTip(TOOL_TIP["save_all"])
        save_all_action.setToolTip(TOOL_TIP["save_all"])
        save_all_action.triggered.connect(self.save_all_files)
        
        # only make each action once, otherwise shortcuts are ambiguous
        if (not hasattr(self, "_save_actions")):
            self._save_actions = list()
            self._save_actions.append(save_action)
            self._save_actions.append(save_as_action)
            self._save_actions.append(save_all_action)

        return self._save_actions        

    def output_actions(self):
        export_html_action = QtGui.QAction(
            USER_TEXT["export_html"], 
            self
            )
        export_html_action.setIcon(
            QtGui.QIcon(Configuration.IMAGES["export_html"])
            )
        export_html_action.setStatusTip(TOOL_TIP["export_html"])
        export_html_action.setToolTip(TOOL_TIP["export_html"])
        export_html_action.triggered.connect(self.export_html)

        export_pdf_action = QtGui.QAction(
            USER_TEXT["export_pdf"], 
            self
            )
        export_pdf_action.setIcon(
            QtGui.QIcon(Configuration.IMAGES["export_pdf"])
            )
        export_pdf_action.setStatusTip(TOOL_TIP["export_pdf"])
        export_pdf_action.setToolTip(TOOL_TIP["export_pdf"])
        export_pdf_action.triggered.connect(self.export_pdf)

        print_action = QtGui.QAction(
            USER_TEXT["print"], 
            self
            )
        print_action.setIcon(QtGui.QIcon(Configuration.IMAGES["print"]))
        print_action.setStatusTip(TOOL_TIP["print_menu"])
        print_action.setToolTip(TOOL_TIP["print_menu"])
        print_action.setMenu(self.print_menu())

        # only make each action once, otherwise shortcuts are ambiguous
        if (not hasattr(self, "_output_actions")):
            self._output_actions = list()
            self._output_actions.append(export_html_action)
            self._output_actions.append(export_pdf_action)
            self._output_actions.append(print_action)

        return self._output_actions

    def print_dialog(self, print_function):
        if (self.editor.count()):
            printer = QtGui.QPrinter()
            printer_dialog = QtGui.QPrintDialog(printer, self)
            result = printer_dialog.exec_()
            if (result == QtGui.QDialog.Accepted):
                print_function(printer)

    def print_markdown_dialog(self):
        self.print_dialog(self.print_markdown)

    def print_rendered_html_dialog(self):
        self.print_dialog(self.print_rendered_html)

    def print_raw_html_dialog(self):
        self.print_dialog(self.print_raw_html)

    def print_markdown(self, printer):
        self.editor.currentWidget().text.print_(printer)

    def print_preview_markdown(self):
        self.print_preview_dialog(self.print_markdown)

    def print_preview_rendered_html(self):
        self.print_preview_dialog(self.print_rendered_html)

    def print_preview_raw_html(self):
        self.print_preview_dialog(self.print_raw_html)

    def print_preview_dialog(self, print_function):
        if (self.editor.count()):
            printer = QtGui.QPrinter()
            preview = QtGui.QPrintPreviewDialog(printer, self)
            filename = self.editor.currentWidget().filename
            if (filename):
                preview.setWindowTitle(filename)
            preview.resize(800, 1000)
            preview.paintRequested.connect(print_function)
            preview.exec_()

    def print_rendered_html(self, printer):
        self.editor.currentWidget().output.print_(printer)

    def print_raw_html(self, printer):
        original = Configuration.OPTIONS["show_html"]
        Configuration.OPTIONS["show_html"] = True
        self.editor.currentWidget().reload()
        self.editor.currentWidget().output.print_(printer)
        Configuration.OPTIONS["show_html"] = original
        self.editor.currentWidget().reload()

    def raise_configure_dialog(self):
        config_dialog = ConfigurationDialog.ConfigurationDialog(self)
        config_dialog.exec_()
        for i in range(self.editor.count()):
            self.editor.widget(i).set_font()
            self.editor.widget(i).reload()
            
    def raise_find_dialog(self):
        find_dialog = FindDialog(self)
        find_dialog.show()

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

    def insert_link(self):
        if (self.editor.count()):
            link, link_ok = QtGui.QInputDialog.getText(
                self,
                USER_TEXT["insert_link"],
                USER_TEXT["enter_link"]
                )
            if (link_ok):
                self.editor.currentWidget().insert_link(unicode(link))

    def link_image(self):
        if (self.editor.count()):
            dialog = ImageDialog(self)
            ok_clicked, image_location, title = dialog.get_image()
            if (ok_clicked):
                self.editor.currentWidget().link_image(image_location, title)

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
        document = Document(self, self.document_changed)
        self.editor.addTab(document, "")
        self.editor.setCurrentIndex(self.editor.count() - 1)
        self.set_tab_title()

    def export_pdf(self):
        if (self.editor.count()):
            location = "."
            if (self.editor.currentWidget().file_path):
                location, ext = os.path.splitext(
                    unicode(self.editor.currentWidget().file_path)
                    )
                location = location + ".pdf"
            file_path = QtGui.QFileDialog.getSaveFileName(
                self,
                USER_TEXT["export_pdf"],
                location,
                "PDF (*.pdf)"
                )
            if (file_path):
                QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                printer = QtGui.QPrinter()
                printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
                printer.setOutputFileName(file_path)
                self.print_rendered_html(printer)
                QtGui.QApplication.restoreOverrideCursor()

    def export_html(self):
        if (self.editor.count()):
            location = "."
            if (self.editor.currentWidget().file_path):
                location, ext = os.path.splitext(
                    unicode(self.editor.currentWidget().file_path)
                    )
                location = location + ".html"
            file_path = QtGui.QFileDialog.getSaveFileName(
                self,
                USER_TEXT["export_html"],
                location,
                "HTML (*.html)"
                )
            if (file_path):
                self.editor.currentWidget().export_html(file_path)

    def close_file(self):
        """
        Removes the tab, if unsaved confirms either save or close without 
        saving.

        returns whether the file was closed.
        """
        if (not self.editor.count()):
            # there is no tab, so close the program
            self.close()
        else:
            if (not self.editor.currentWidget().saved):
                action = self.confirm_close_file()
                if (action == QtGui.QMessageBox.Save):
                    self.save_file()
                elif (action == QtGui.QMessageBox.Cancel):
                    return False
            self.editor.removeTab(self.editor.currentIndex())
            return True


    def confirm_close_file(self):
        """
        Asks the user whether they want to close the file.
        returns the action
        """
        # have a dialog here for saving current tab
        # do you want to save the changes you've made to [file_path]
        # yes/no/cancel
        confirm_dialog = QtGui.QMessageBox(self)
        confirm_dialog.setWindowTitle(
            USER_TEXT["program_name"]
            )
        document = self.editor.currentWidget()
        message = [
            USER_TEXT["made_changes"],
            " "
            ]
        
        if (document.filename):
            message.append(document.filename)
        else:
            message.append(USER_TEXT["current_document"])
            
        confirm_dialog.setText("".join(message))
        confirm_dialog.setInformativeText(
            USER_TEXT["save_changes?"]
            )
        confirm_dialog.setStandardButtons(
            QtGui.QMessageBox.Save | 
            QtGui.QMessageBox.Discard | 
            QtGui.QMessageBox.Cancel
            )
        confirm_dialog.setDefaultButton(QtGui.QMessageBox.Save)
        return confirm_dialog.exec_()

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
                    USER_TEXT["saved"],
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
                USER_TEXT["saved"], 
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
            USER_TEXT["open_file"],
            ".",
            Configuration.MARKDOWN_FILE_STRING
            )
        if (file_path):
            self.open_file(file_path)

    def open_file(self, file_path):
        document = Document(self, self.document_changed)
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
            self.set_tab_title()

#==============================================================================
class ColourButton(QtGui.QToolButton):

    def __init__(self, parent, set_colour):
        super(ColourButton, self).__init__(parent)

        self.set_colour = set_colour
        self.colour = "#ff0000"
        
        self.setToolTip(TOOL_TIP["set_colour"])
        self.setStatusTip(TOOL_TIP["set_colour"])
        self.clicked.connect(
            lambda : self.set_colour(self.colour)
            )
        self.setIcon(
            QtGui.QIcon(Configuration.IMAGES["letter"])
            )
        
        menu = QtGui.QMenu(self)
        self.setMenu(menu)
        menu.aboutToShow.connect(self.colour_dialog)

        self.setPopupMode(QtGui.QToolButton.MenuButtonPopup)

        self.update_ui()

    def update_ui(self):
        style = [
            "QToolButton {",
            "border-style: outset;",
            "border: 1px solid gray;",
            "border-radius: 5px;",
            "font: bold 14px;",
            "width: 27px;",
            "height: 20px;",
            "background-color: ",
            self.colour,
            ";} ",
            # Set the style for the menu part of the button
            "QToolButton::menu-button {",
            "background-color: beige;",
            "border-style: outset;",
            "border: 2px solid gray;",
            "border-top-right-radius: 5px;",
            "border-bottom-right-radius: 5px;",
            "width: 9px;",
            "height: 21px;",
            "}",
            ]
        self.setStyleSheet("".join(style))

    def colour_dialog(self):
        self.menu().hide()
        colour = QtGui.QColorDialog.getColor()
        if (colour.isValid()):
            self.colour = unicode(colour.name())
            self.update_ui()
            self.set_colour(self.colour)
        self.menu().setVisible(False)
        
#==============================================================================
class ImageDialog(QtGui.QDialog):

    def __init__(self, parent):
        super(ImageDialog, self).__init__(parent)
        
        self.accepted = False

        self.initialise_ui()
        self.exec_()

    def initialise_ui(self):
        enter_image_label = QtGui.QLabel(
            USER_TEXT["enter_image_location"]
            )
        self.image_entry = QtGui.QLineEdit()
        enter_image_label.setBuddy(self.image_entry)
        browse_for_image = QtGui.QPushButton(
            USER_TEXT["browse_for_image"]
            )
        browse_for_image.clicked.connect(self.browse_for_image)

        title_label = QtGui.QLabel(
            USER_TEXT["enter_image_title"]
            )
        self.title_entry = QtGui.QLineEdit()
        title_label.setBuddy(self.title_entry)

        # add a save and a cancel button
        bottom_buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok |  QtGui.QDialogButtonBox.Cancel
            )
        bottom_buttons.accepted.connect(self.accept)
        bottom_buttons.rejected.connect(self.close)
        
        line_layout = QtGui.QHBoxLayout()
        line_layout.addWidget(enter_image_label)
        line_layout.addWidget(self.image_entry)

        button_layout = QtGui.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(browse_for_image)

        image_entry_layout = QtGui.QVBoxLayout()
        image_entry_layout.addLayout(line_layout)
        image_entry_layout.addLayout(button_layout)

        title_layout = QtGui.QHBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_entry)
        
        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(image_entry_layout)
        main_layout.addLayout(title_layout)
        main_layout.addWidget(bottom_buttons)

        self.setLayout(main_layout)

        self.setWindowTitle(USER_TEXT["link_image"])

    def browse_for_image(self):
        file_path = QtGui.QFileDialog.getOpenFileName(
            self,
            USER_TEXT["browse_for_image"],
            ".",
            Configuration.IMAGE_FILE_STRING
            )
        if (file_path):
            self.image_entry.setText(file_path)

    def accept(self):
        self.accepted = True
        self.close()

    def get_image(self):
        """
        Raises the form and returns a tuple 
        (ok_clicked, image_location, title)
        """
        image_location = unicode(self.image_entry.text())
        title = unicode(self.title_entry.text())
        return (self.accepted, image_location, title)

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
class MarkdownPreview(QtWebKit.QWebView):

    def __init__(self, parent):
        super(MarkdownPreview, self).__init__(parent)
        self.parent = parent
        self.displayed_page = QtWebKit.QWebPage()
        self.displayed_page.setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.displayed_page.linkHovered.connect(self.link_hovered)
        self.setPage(self.displayed_page)
        self.linkClicked.connect(open_link)
        self.scroll_x = 0

    def link_hovered(self, link, title, text_content):
        if (not link and not title and not text_content):
            self.emit(QtCore.SIGNAL("mouse_left_link"))
        else:
            self.emit(QtCore.SIGNAL("mouse_over_link"), link)

    def show_preview(self, html):
        if (Configuration.OPTIONS["show_html"]):
            html = "".join(
                [
                    "<pre><code>",
                    cgi.escape(html),
                    "</code></pre>"
                    ]
                )
        self.setHtml(html)

    def scroll_position(self):
        frame = self.page().mainFrame()
        x_current = frame.scrollPosition().x()
        x_maximum = frame.scrollBarMaximum(QtCore.Qt.Horizontal)
        if (x_maximum == 0):
            x_maximum = 1
        y_current = frame.scrollPosition().y()
        y_maximum = frame.scrollBarMaximum(QtCore.Qt.Vertical)
        if (y_maximum == 0):
            y_maximum = 1
        return (x_current / float(x_maximum), y_current / float(y_maximum))

    def set_scroll_position(self, ratios):
        """
        Ratio should be a pair of numbers between 0 and 1. x then y
        """
        frame = super(MarkdownPreview, self).page().mainFrame()
        x_value = ratios[0] * frame.scrollBarMaximum(QtCore.Qt.Horizontal)
        y_value = ratios[1] * frame.scrollBarMaximum(QtCore.Qt.Vertical)
        point = QtCore.QPoint(x_value, y_value)
        frame.setScrollPosition(point)

    def __del__(self):
        # For some reason without this, when you quit the application it 
        # restarts itself, I think it's to do with ref counts on the page
        del self.displayed_page
        
#==============================================================================
class Document(QtGui.QWidget):

    def __init__(self, parent, callback):
        super(Document, self).__init__(parent)

        self.file_path = None
        self.saved = True

        self.callback = callback
        self.edit_time = 0
        
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.text_changed)

        self.text = QtGui.QTextEdit(self)
        self.text.verticalScrollBar().valueChanged.connect(
            lambda value : self.sync_scrollbars()
            )
        self.text.setAcceptRichText(False)
        self.text.textChanged.connect(self.reload)
        
        self.output = MarkdownPreview(self)
        QtCore.QObject.connect(
            self.output,
            QtCore.SIGNAL("mouse_over_link"),
            lambda link: parent.statusBar().showMessage(link)
            )
        QtCore.QObject.connect(
            self.output,
            QtCore.SIGNAL("mouse_left_link"),
            parent.statusBar().clearMessage
            )

        self.set_font()

        self.horizontal_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        self.horizontal_splitter.addWidget(self.text)
        self.horizontal_splitter.addWidget(self.output)
        self.size_set = False

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.horizontal_splitter)

    def showEvent(self, event):
        super(Document, self).showEvent(event)
        if (not self.size_set):
            self.set_horizontal_sizes()

    def set_horizontal_sizes(self):
        size = self.horizontal_splitter.frameSize()
        half_width = size.width() / 2
        self.horizontal_splitter.setSizes([half_width, half_width])
        self.size_set = True

    @property
    def filename(self):
        if (self.file_path is not None):
            return os.path.basename(unicode(self.file_path))

    def sync_scrollbars(self):
        max_text_scroll = self.text.verticalScrollBar().maximum()
        if (max_text_scroll):
            value = self.text.verticalScrollBar().value()
            ratio = float(value) / max_text_scroll
            self.output.set_scroll_position((0, ratio))

    def check_saved(self):
        if (self.file_path is not None):
            with open(self.file_path, "r") as current_file:
                content = current_file.read()
            self.saved = self.text.toPlainText() == content
        else:
            self.saved = False

    def set_font(self):
        config_font = Configuration.OPTIONS["font"]
        font = QtGui.QFont()
        font.fromString(config_font)
        self.text.setFont(font)

    def text_changed(self):
        """
        We don't want to update on every keystroke, what this does is:
          1. Times how long a reload takes
          2. After reload start a timer for the duration that the reload took
          3. If the timer is running, don't reload
          4. If the time is not running go to 1.
        """
        if (not self.timer.isActive()):
            t_start = time.time()
            self.reload()
            self.edit_time = time.time() - t_start
            # self.edit_time is in seconds, timer wants milliseconds
            self.timer.start(self.edit_time * 1000)
        
    def reload(self):
        html = self.convert_input()
        scroll_position = self.output.scroll_position()
        self.output.show_preview(html)
        self.output.set_scroll_position(scroll_position)
        self.check_saved()
        self.sync_scrollbars()
        self.callback()

    def convert_input(self):
        markdown_string = self.text.toPlainText()
        return process_markdown(unicode(markdown_string))

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

    def insert_link(self, link):
        self.edit_selection("[", "]", False)
        cursor = self.text.textCursor()
        text = cursor.selectedText()
        text.append("".join(["(", link, ")"]))
        cursor.insertText(text)

    def link_image(self, image_location, title):
        self.edit_selection("![", "]", False)
        cursor = self.text.textCursor()
        text = cursor.selectedText()
        text.append("".join(["(", image_location, " \"", title, "\")"]))
        cursor.insertText(text)

    def edit_selection(self, beginning, end, needs_selection=True):
        """
        Do an edit to the current selection. Add beginning to the start and end
        to the end.
        
        needs selection governs whether if the selection is empty it will 
        insert anything.
        """
        cursor = self.text.textCursor()
        if (not needs_selection or cursor.hasSelection()):
            text = cursor.selectedText()
            text.prepend(beginning)
            text.append(end)
            cursor.insertText(text)

#==============================================================================
class PreviewDialog(QtGui.QDialog):

    def __init__(self, parent, title, markdown):
        super(PreviewDialog, self).__init__(parent)
        self.setWindowTitle(title)
        preview = MarkdownPreview(self)
        preview.show_preview(process_markdown(markdown))

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(preview)

#==============================================================================
class Help(object):

    def open_link(self):
        open_link(
            QtCore.QUrl("https://bitbucket.org/davidcorne/markdown-editor")
            )

    def open_description(self, markdown_type, description):
        # Make sure the specific markdown help is rendered in the proper 
        # variety of markdown
        processor = Configuration.OPTIONS["processor"]
        Configuration.OPTIONS["processor"] = markdown_type
        Configuration.load_processor()
        self.help_dialog = PreviewDialog(
            None,
            USER_TEXT[markdown_type],
            description
            )
        self.help_dialog.show()
        Configuration.OPTIONS["processor"] = processor
        Configuration.load_processor()

    def markdown_description(self):
        self.open_description("markdown", Examples.STANDARD_MARKDOWN)

    def markdown_extra_description(self):
        self.open_description("markdown_extra", Examples.MARKDOWN_EXTRA)

    def markdown_all_description(self):
        self.open_description("markdown_all", Examples.MARKDOWN_ALL)

    def codehilite_description(self):
        self.open_description("codehilite", Examples.CODEHILITE)
        
    def github_description(self):
        self.open_description(
            "github_flavoured_markdown",
            Examples.GITHUB_FLAVOUR_PREVIEW
            )
        
#==============================================================================
def open_link(url):
    """
    Takes a QtCore.QUrl
    """
    ok = QtGui.QDesktopServices.openUrl(url)
    if (not ok):
        detail = ["Could not find location:", unicode(url.toString())]
        Error.show_error("Failed to open URL", "\n\n".join(detail))

#==============================================================================
def process_markdown(markdown_string):
    return Configuration.PROCESSOR.render(markdown_string)

#==============================================================================
if (__name__ == "__main__"):
    pass
