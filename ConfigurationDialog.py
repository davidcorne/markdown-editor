#!/usr/bin/env python
# Written by: DGC

# python imports

import copy

from PyQt4 import QtGui, QtCore

# local imports

import Configuration
import Processor

#==============================================================================
class MarkdownConfig(QtGui.QDialog):

    def __init__(self, parent, config):
        super(MarkdownConfig, self).__init__(parent)
        self.config = config
        self.markdown_types = Configuration.PROCESSOR_TYPES.keys()

        config_group = QtGui.QGroupBox(
            Configuration.USER_TEXT["markdown_type"]
            )

        markdown_label = QtGui.QLabel(Configuration.USER_TEXT["markdown"])

        markdown_combo = QtGui.QComboBox()
        for markdown_type in Configuration.PROCESSOR_TYPES.keys():
            markdown_combo.addItem(markdown_type)
        # select the currently used processor, not particularly pleasent
        selected_processor = Configuration.PROCESSOR.__class__
        index = Configuration.PROCESSOR_TYPES.values().index(
            selected_processor
            )
        markdown_combo.setCurrentIndex(index) 
        self.markdown_type = self.markdown_types[index]
        markdown_combo.currentIndexChanged["QString"].connect(
            self.new_markdown_chosen
            )

        markdown_layout = QtGui.QHBoxLayout()
        markdown_layout.addWidget(markdown_label)
        markdown_layout.addWidget(markdown_combo)

        config_layout = QtGui.QVBoxLayout()
        config_layout.addLayout(markdown_layout)
        config_group.setLayout(config_layout)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(config_group)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def new_markdown_chosen(self, markdown_type):
        self.markdown_type = str(markdown_type)
    
    def save(self):
        new_processor = Configuration.PROCESSOR_TYPES[self.markdown_type]()
        Configuration.PROCESSOR = new_processor

#==============================================================================
class MiscConfig(QtGui.QDialog):

    def __init__(self, parent, config):
        super(MiscConfig, self).__init__(parent)
        self.config = config
        
        config_group = QtGui.QGroupBox(Configuration.USER_TEXT["debug_options"])

        show_html = QtGui.QCheckBox(Configuration.USER_TEXT["show_html"])
        if (self.config["show_html"]):
            show_html.setCheckState(QtCore.Qt.Checked)
        else:
            show_html.setCheckState(QtCore.Qt.Unchecked) 
        show_html.stateChanged.connect(self.show_html_changed)

        group_layout = QtGui.QVBoxLayout()
        group_layout.addWidget(show_html)

        config_group.setLayout(group_layout)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(config_group)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def show_html_changed(self, value):
        self.config["show_html"] = value

    def save(self):
        pass
    
#==============================================================================
class ConfigurationDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ConfigurationDialog, self).__init__(parent)

        self.config = copy.copy(Configuration.OPTIONS)

        self.contents = QtGui.QListWidget()
        self.contents.setViewMode(QtGui.QListView.IconMode)
        self.contents.setIconSize(QtCore.QSize(96, 84))
        self.contents.setMovement(QtGui.QListView.Static)
        self.contents.setMaximumWidth(128)
        self.contents.setSpacing(12)

        self.pages = QtGui.QStackedWidget()
        self.pages.addWidget(MarkdownConfig(self, self.config))
        self.pages.addWidget(MiscConfig(self, self.config))

        # add a save and a cancel button
        bottom_buttons = QtGui.QDialogButtonBox(
             QtGui.QDialogButtonBox.Save |  QtGui.QDialogButtonBox.Cancel
            )
        bottom_buttons.accepted.connect(self.save_and_close)
        bottom_buttons.rejected.connect(self.close)

        self.create_icons()
        self.contents.setCurrentRow(0)

        horizontal_layout = QtGui.QHBoxLayout()
        horizontal_layout.addWidget(self.contents)
        horizontal_layout.addWidget(self.pages, 1)

        buttons_layout = QtGui.QHBoxLayout()
        buttons_layout.addWidget(bottom_buttons)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(horizontal_layout)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        self.setWindowTitle(Configuration.USER_TEXT["options"])
        self.exec_()

    def save_and_close(self):
        for index in range(self.pages.count()):
            self.pages.widget(index).save()
        for key in self.config:
            Configuration.OPTIONS[key] = self.config[key]
        self.close()

    def change_page(self, current, previous):
        if not current:
            current = previous

        self.pages.setCurrentIndex(self.contents.row(current))

    def create_icons(self):
        markdown_button = QtGui.QListWidgetItem(self.contents)
        markdown_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["markdown"])
            )
        markdown_button.setText(Configuration.USER_TEXT["markdown"])
        markdown_button.setTextAlignment(QtCore.Qt.AlignHCenter)
        markdown_button.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
            )

        misc_button = QtGui.QListWidgetItem(self.contents)
        misc_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["configure"])
            )
        misc_button.setText(Configuration.USER_TEXT["misc"])
        misc_button.setTextAlignment(QtCore.Qt.AlignHCenter)
        misc_button.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
            )

        self.contents.currentItemChanged.connect(self.change_page)

#==============================================================================
if (__name__ == "__main__"):
    pass
