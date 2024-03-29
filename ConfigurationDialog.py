#!/usr/bin/env python
# Written by: DGC

# python imports
from __future__ import unicode_literals

import copy
import logging
import os

from PyQt4 import QtGui, QtCore

# local imports

import Configuration
import Examples
import Log
import MarkdownEditor
import Resources

from UserText import USER_TEXT

#==============================================================================
class MarkdownConfig(QtGui.QDialog):

    def __init__(self, parent, reload_callback):
        super(MarkdownConfig, self).__init__(parent)
        
        self.reload_callback = reload_callback
        self.original_processor = Configuration.PROCESSOR

        config_group = QtGui.QGroupBox(
            USER_TEXT["markdown_type"]
            )

        markdown_label = QtGui.QLabel(USER_TEXT["markdown"])

        markdown_combo = QtGui.QComboBox()
        for markdown_type in Configuration.PROCESSOR_TYPES.keys():
            markdown_combo.addItem(USER_TEXT[markdown_type])
        index = Configuration.PROCESSOR_TYPES.keys().index(
            Configuration.OPTIONS["processor"]
            )
        markdown_combo.setCurrentIndex(index) 
        markdown_combo.currentIndexChanged.connect(
            self.new_markdown_chosen
            )

        self.preview = Preview()
        
        markdown_layout = QtGui.QHBoxLayout()
        markdown_layout.addWidget(markdown_label)
        markdown_layout.addWidget(markdown_combo)

        config_layout = QtGui.QVBoxLayout()
        config_layout.addLayout(markdown_layout)
        config_group.setLayout(config_layout)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(config_group)
        main_layout.addWidget(self.preview)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def new_markdown_chosen(self, index):
        types = Configuration.PROCESSOR_TYPES
        Configuration.OPTIONS["processor"] = types.keys()[index]
        Configuration.load_processor()
        self.reload_callback()
    
    def reload_preview(self):
        self.preview.reload()

    def revert(self):
        Configuration.PROCESSOR = self.original_processor

#==============================================================================
class CSSConfig(QtGui.QDialog):

    def __init__(self, parent, reload_callback):
        super(CSSConfig, self).__init__(parent)
       
        self.reload_callback = reload_callback
        css_group = QtGui.QGroupBox(
            USER_TEXT["style_name"]
            )
        markdown_css_label = [
            USER_TEXT["markdown"],
            " ",
            USER_TEXT["css"],
            ]
        markdown_css_label = QtGui.QLabel("".join(markdown_css_label))

        markdown_css_combo = self.find_markdown_css_options()

        markdown_css_layout = QtGui.QHBoxLayout()
        markdown_css_layout.addWidget(markdown_css_label)
        markdown_css_layout.addWidget(markdown_css_combo)

        code_css_label = [
            USER_TEXT["code"],
            " ",
            USER_TEXT["css"],
            ]
        code_css_label = QtGui.QLabel("".join(code_css_label))

        code_css_combo = self.find_code_css_options()

        self.preview = Preview()

        code_css_layout = QtGui.QHBoxLayout()
        code_css_layout.addWidget(code_css_label)
        code_css_layout.addWidget(code_css_combo)

        config_layout = QtGui.QVBoxLayout()
        config_layout.addLayout(markdown_css_layout)
        config_layout.addLayout(code_css_layout)
        css_group.setLayout(config_layout)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(css_group)
        main_layout.addWidget(self.preview)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def find_code_css_options(self):
        css_combo = QtGui.QComboBox()
        css_combo.addItem("None")
        css_files = self.find_css_files("Code")
        for md_file in css_files:
            css_combo.addItem(md_file)
        # add one for None
        if (Configuration.OPTIONS["code_css"]):
            css_combo.setCurrentIndex(
                css_files.index(Configuration.OPTIONS["code_css"]) + 1
            )
        css_combo.currentIndexChanged["QString"].connect(
            self.new_code_css_chosen
            )

        return css_combo

    def new_code_css_chosen(self, css):
        if (css == "None"):
            css = ""
        Configuration.OPTIONS["code_css"] = unicode(css)
        Configuration.load_code_css()
        self.reload_callback()

    def find_markdown_css_options(self):
        css_combo = QtGui.QComboBox()
        css_combo.addItem("None")
        css_files = self.find_css_files("Markdown")
        for md_file in css_files:
            css_combo.addItem(md_file)
        # add one for None
        if (Configuration.OPTIONS["markdown_css"]):
            css_combo.setCurrentIndex(
                css_files.index(Configuration.OPTIONS["markdown_css"]) + 1
            )
        css_combo.currentIndexChanged["QString"].connect(
            self.new_markdown_css_chosen
            )

        return css_combo

    def find_css_files(self, directory):
        """
        Directory should be a directory below Resources/CSS
        """
        css_dir = os.path.join(Resources.directory(), "CSS")
        css_dir = os.path.join(css_dir, directory)
        css_files = [s for s in os.listdir(css_dir) if s.endswith(".css")]
        user_css_dir = os.path.join(css_dir, "User")
        logging.info("Looking for CSS directory: \"%s\"", user_css_dir)
        if (os.path.isdir(user_css_dir)):
            user_css_files = [s for s in os.listdir(user_css_dir) if s.endswith(".css")]
            logging.info(
                "User %s CSS files \"%s\" found at path: %s",
                directory,
                str(user_css_files),
                user_css_dir
                )
            css_files += user_css_files
        css_files = [os.path.splitext(md_file)[0] for md_file in css_files]
        return css_files

    def reload_preview(self):
        self.preview.reload()

    def new_markdown_css_chosen(self, css):
        if (css == "None"):
            css = ""
        Configuration.OPTIONS["markdown_css"] = unicode(css)
        Configuration.load_markdown_css()
        self.reload_callback()

    def revert(self):
        Configuration.load_markdown_css()
        Configuration.load_code_css()

#==============================================================================
class MiscConfig(QtGui.QDialog):

    def __init__(self, parent, localisation, reload_callback):
        self.localisation = localisation
        super(MiscConfig, self).__init__(parent)
        self.reload_callback = reload_callback
        
        display_group = QtGui.QGroupBox(
            USER_TEXT["display_options"]
            )
        font_dialog_button = QtGui.QPushButton(
            USER_TEXT["change_font"]
            )
        font_dialog_button.clicked.connect(self.raise_font_dialog)

        font_dialog_layout = QtGui.QHBoxLayout()
        font_dialog_layout.addWidget(font_dialog_button)
        font_dialog_layout.addStretch()

        display_layout = QtGui.QVBoxLayout()
        display_layout.addLayout(font_dialog_layout)

        display_group.setLayout(display_layout)

        debug_group = QtGui.QGroupBox(
            USER_TEXT["debug_options"]
            )
        
        show_html = self.check_box(
            USER_TEXT["show_html"],
            self.show_html_changed,
            Configuration.OPTIONS["show_html"]
            )

        log_file_location_label = QtGui.QLabel(USER_TEXT["log_file_location"])
        log_file_location = QtGui.QLabel(Log.log_file())
        log_file_location.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse | QtCore.Qt.TextSelectableByKeyboard
            )
        log_file_layout =  QtGui.QHBoxLayout()
        log_file_layout.addWidget(log_file_location_label)
        log_file_layout.addWidget(log_file_location)
        log_file_layout.addStretch(1)

        debug_layout = QtGui.QVBoxLayout()
        debug_layout.addWidget(show_html)
        debug_layout.addLayout(log_file_layout)

        debug_group.setLayout(debug_layout)


        other_group = QtGui.QGroupBox(
            USER_TEXT["other_options"]
            )

        show_line_numbers = self.check_box(
            USER_TEXT["show_line_numbers"],
            self.show_line_numbers_changed,
            Configuration.OPTIONS["display_line_numbers"]
            )

        css_class_input = QtGui.QLineEdit(
            Configuration.OPTIONS["code_css_class"]
            )
        css_class_input.textChanged.connect(self.css_class_changed)
        css_class_label = QtGui.QLabel(
            USER_TEXT["code_css_class"]
            )
        self.original_css_class = Configuration.OPTIONS["code_css_class"]
        
        css_class_layout = QtGui.QHBoxLayout()
        css_class_layout.addWidget(css_class_input)
        css_class_layout.addWidget(css_class_label)
        css_class_layout.addStretch(1)

        
        language_group = QtGui.QGroupBox(USER_TEXT["change_language"])
        language_layout = QtGui.QHBoxLayout()
        languages = [
            ("united_kingdom", "en_GB"), 
            ("united_states", "en_US"),
            ("australia", "en_AU"),
            ("france", "fr_FR"),
            ("germany", "de_DE"),
        ]
        for icon, locale in languages:
            language_button = QtGui.QPushButton()
            language_button.setIcon(QtGui.QIcon(Configuration.IMAGES[icon]))
            language_button.clicked.connect(
                lambda val, locale=locale: self.change_locale(locale)
            )
            language_layout.addWidget(language_button)
        language_layout.addStretch(1)
        language_group.setLayout(language_layout)

        self.original_locale = self.localisation.language()
        
        other_layout = QtGui.QVBoxLayout()
        other_layout.addWidget(show_line_numbers)
        other_layout.addLayout(css_class_layout)
        
        other_group.setLayout(other_layout)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(display_group)
        main_layout.addWidget(language_group)
        main_layout.addWidget(other_group)
        main_layout.addWidget(debug_group)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def change_locale(self, locale):
        self.localisation.set_language(locale)
        QtGui.QMessageBox.information(
            self,
            USER_TEXT["restart"],
            USER_TEXT["restart_effect"]
        )

    def css_class_changed(self, value):
        Configuration.OPTIONS["code_css_class"] = unicode(value)
        self.reload_callback()

    def show_html_changed(self, value):
        Configuration.OPTIONS["show_html"] = value
        self.reload_callback()

    def show_line_numbers_changed(self, value):
        Configuration.OPTIONS["display_line_numbers"] = bool(value)
        self.reload_callback()

    def check_box(self, name, callback, checked):
        """
        Returns a Qt checkbox with the specified name, bound to the function
        and checked.
        """
        check_box = QtGui.QCheckBox(name)
        if (checked):
            check_box.setCheckState(QtCore.Qt.Checked)
        else:
            check_box.setCheckState(QtCore.Qt.Unchecked) 
        check_box.stateChanged.connect(callback)
        return check_box

    def raise_font_dialog(self):
        config_font = Configuration.OPTIONS["font"]
        current_font = QtGui.QFont()
        current_font.fromString(config_font)
        font, ok = QtGui.QFontDialog.getFont(
            current_font,
            self,
            USER_TEXT["change_font"]
            )
        if (ok):
            Configuration.OPTIONS["font"] = font.toString()

    def revert(self):
        Configuration.OPTIONS["code_css_class"] = self.original_css_class
        self.change_locale(self.original_locale)
    
#==============================================================================
class ConfigurationDialog(QtGui.QDialog):

    OPEN_PAGE = 0

    def __init__(self, parent, localisation):
        super(ConfigurationDialog, self).__init__(parent)

        self.original_config = copy.copy(Configuration.OPTIONS)

        self.contents = QtGui.QListWidget()
        self.contents.setViewMode(QtGui.QListView.IconMode)
        self.contents.setIconSize(QtCore.QSize(96, 84))
        self.contents.setMovement(QtGui.QListView.Static)
        self.contents.setMaximumWidth(128)
        self.contents.setSpacing(12)

        self.pages = QtGui.QStackedWidget()
        self.css_config = CSSConfig(self, self.reload_previews)
        self.md_config = MarkdownConfig(self, self.reload_previews)
        self.misc_config = MiscConfig(self, localisation, self.reload_previews)

        self.pages.addWidget(self.md_config)
        self.pages.addWidget(self.css_config)
        self.pages.addWidget(self.misc_config)

        # add a save and a cancel button
        self.bottom_buttons = QtGui.QDialogButtonBox(
             QtGui.QDialogButtonBox.Save |  
             QtGui.QDialogButtonBox.RestoreDefaults | 
             QtGui.QDialogButtonBox.Cancel
            )
        self.bottom_buttons.accepted.connect(self.save_and_close)
        self.bottom_buttons.rejected.connect(self.revert_and_close)

        self.create_icons()
        self.contents.setCurrentRow(ConfigurationDialog.OPEN_PAGE)
        self.contents.currentRowChanged.connect(self.change_page)

        horizontal_layout = QtGui.QHBoxLayout()
        horizontal_layout.addWidget(self.contents)
        horizontal_layout.addWidget(self.pages, 1)

        buttons_layout = QtGui.QHBoxLayout()
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.bottom_buttons)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(horizontal_layout)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        self.setWindowTitle(USER_TEXT["options"])
        self.pages.setCurrentIndex(ConfigurationDialog.OPEN_PAGE)

    def reload_previews(self):
        self.css_config.reload_preview()
        self.md_config.reload_preview()

    def save_and_close(self):
        Configuration.save_options()
        self.close()

    def revert_and_close(self):
        for key in Configuration.OPTIONS:
            Configuration.OPTIONS[key] = self.original_config[key]
        for index in range(self.pages.count()):
            self.pages.widget(index).revert()
        self.close()

    def change_page(self, new_row):
        self.pages.setCurrentIndex(new_row)
        ConfigurationDialog.OPEN_PAGE = new_row

    def create_icons(self):
        markdown_button = QtGui.QListWidgetItem(self.contents)
        markdown_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["markdown"])
            )
        markdown_button.setText(USER_TEXT["markdown"])
        markdown_button.setTextAlignment(QtCore.Qt.AlignHCenter)
        markdown_button.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
            )

        css_button = QtGui.QListWidgetItem(self.contents)
        css_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["css"])
            )
        css_button.setText(USER_TEXT["css"])
        css_button.setTextAlignment(QtCore.Qt.AlignHCenter)
        css_button.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
            )

        misc_button = QtGui.QListWidgetItem(self.contents)
        misc_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["configure"])
            )
        misc_button.setText(USER_TEXT["misc"])
        misc_button.setTextAlignment(QtCore.Qt.AlignHCenter)
        misc_button.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
            )

#==============================================================================
class Preview(QtGui.QGroupBox):

    def __init__(self):
        super(Preview, self).__init__(USER_TEXT["preview"])
        self.preview = MarkdownEditor.MarkdownPreview(None)
        self.reload()

        preview_layout = QtGui.QVBoxLayout()
        preview_layout.addWidget(self.preview)
        self.setLayout(preview_layout)

    def reload(self):
        Configuration.load_processor()
        html = MarkdownEditor.process_markdown(
            Examples.get_preview_markdown(Configuration.OPTIONS["processor"])
            )
        self.preview.show_preview(html)
        
#==============================================================================
if (__name__ == "__main__"):
    pass
