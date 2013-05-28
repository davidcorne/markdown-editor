#!/usr/bin/env python
# Written by: DGC

# python imports
from __future__ import unicode_literals

import copy
import os

from PyQt4 import QtGui, QtCore

# local imports

import Configuration
import MarkdownEditor
import Processor

#==============================================================================
class MarkdownConfig(QtGui.QDialog):

    def __init__(self, parent, reload_callback):
        super(MarkdownConfig, self).__init__(parent)
        
        self.reload_callback = reload_callback
        self.original_processor = Configuration.PROCESSOR

        config_group = QtGui.QGroupBox(
            Configuration.USER_TEXT["markdown_type"]
            )

        markdown_label = QtGui.QLabel(Configuration.USER_TEXT["markdown"])

        markdown_combo = QtGui.QComboBox()
        for markdown_type in Configuration.PROCESSOR_TYPES.keys():
            markdown_combo.addItem(Configuration.USER_TEXT[markdown_type])
        index = Configuration.PROCESSOR_TYPES.keys().index(
            Configuration.OPTIONS["processor"]
            )
        markdown_combo.setCurrentIndex(index) 
        markdown_combo.currentIndexChanged.connect(
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

    def new_markdown_chosen(self, index):
        types = Configuration.PROCESSOR_TYPES
        Configuration.OPTIONS["processor"] = types.keys()[index]
        Configuration.PROCESSOR = Configuration.PROCESSOR_TYPES[
            Configuration.OPTIONS["processor"]
        ]()
        self.reload_callback()
    
    def revert(self):
        Configuration.PROCESSOR = self.original_processor

#==============================================================================
class CSSConfig(QtGui.QDialog):

    def __init__(self, parent):
        super(CSSConfig, self).__init__(parent)
       
        css_group = QtGui.QGroupBox(
            Configuration.USER_TEXT["style_name"]
            )
        markdown_css_label = [
            Configuration.USER_TEXT["markdown"],
            " ",
            Configuration.USER_TEXT["css"],
            ]
        markdown_css_label = QtGui.QLabel("".join(markdown_css_label))

        markdown_css_combo = self.find_markdown_css_options()

        markdown_css_layout = QtGui.QHBoxLayout()
        markdown_css_layout.addWidget(markdown_css_label)
        markdown_css_layout.addWidget(markdown_css_combo)

        code_css_label = [
            Configuration.USER_TEXT["code"],
            " ",
            Configuration.USER_TEXT["css"],
            ]
        code_css_label = QtGui.QLabel("".join(code_css_label))

        code_css_combo = self.find_code_css_options()

        preview_group = QtGui.QGroupBox(
            Configuration.USER_TEXT["preview"]
            )
        self.preview = MarkdownEditor.MarkdownPreview(None)
        self.reload_preview()

        code_css_layout = QtGui.QHBoxLayout()
        code_css_layout.addWidget(code_css_label)
        code_css_layout.addWidget(code_css_combo)

        config_layout = QtGui.QVBoxLayout()
        config_layout.addLayout(markdown_css_layout)
        config_layout.addLayout(code_css_layout)
        css_group.setLayout(config_layout)

        preview_layout = QtGui.QVBoxLayout()
        preview_layout.addWidget(self.preview)
        preview_group.setLayout(preview_layout)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(css_group)
        main_layout.addWidget(preview_group)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def find_code_css_options(self):
        css_combo = QtGui.QComboBox()
        css_combo.addItem("None")
        css_dir = os.path.join(Configuration.resource_dir(), "CSS/Code")
        css_files = [s for s in os.listdir(css_dir) if s.endswith(".css")]
        css_files = [os.path.splitext(md_file)[0] for md_file in css_files]
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
        Configuration.reload_code_css()
        self.reload_preview()

    def find_markdown_css_options(self):
        css_combo = QtGui.QComboBox()
        css_combo.addItem("None")
        css_dir = os.path.join(Configuration.resource_dir(), "CSS/Markdown")
        css_files = [s for s in os.listdir(css_dir) if s.endswith(".css")]
        css_files = [os.path.splitext(md_file)[0] for md_file in css_files]
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

    def reload_preview(self):
        html = MarkdownEditor.process_markdown("""\
# Heading 1 #

Some text

## Heading 2 ##

More text

### python ###

This is a python function.  

```python
def hi():
    print("Hi")
```
### C++ ###

This is the same function in C++.  

```c++
#include <iostream>

void hi() 
{
  std::cout << "Hi" << std::endl;
}
```
""")
        self.preview.show_preview(html)

    def new_markdown_css_chosen(self, css):
        if (css == "None"):
            css = ""
        Configuration.OPTIONS["markdown_css"] = unicode(css)
        Configuration.reload_markdown_css()
        self.reload_preview()

    def revert(self):
        Configuration.reload_markdown_css()
        Configuration.reload_code_css()

#==============================================================================
class MiscConfig(QtGui.QDialog):

    def __init__(self, parent, reload_callback):
        super(MiscConfig, self).__init__(parent)
        self.reload_callback = reload_callback
        
        config_group = QtGui.QGroupBox(
            Configuration.USER_TEXT["debug_options"]
            )

        show_html = QtGui.QCheckBox(Configuration.USER_TEXT["show_html"])
        if (Configuration.OPTIONS["show_html"]):
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
        Configuration.OPTIONS["show_html"] = value
        self.reload_callback()

    def revert(self):
        pass
    
#==============================================================================
class ConfigurationDialog(QtGui.QDialog):

    OPEN_PAGE = 0

    def __init__(self, parent=None):
        super(ConfigurationDialog, self).__init__(parent)

        self.original_config = copy.copy(Configuration.OPTIONS)

        self.contents = QtGui.QListWidget()
        self.contents.setViewMode(QtGui.QListView.IconMode)
        self.contents.setIconSize(QtCore.QSize(96, 84))
        self.contents.setMovement(QtGui.QListView.Static)
        self.contents.setMaximumWidth(128)
        self.contents.setSpacing(12)

        self.pages = QtGui.QStackedWidget()
        css_config = CSSConfig(self)
        md_config = MarkdownConfig(self, css_config.reload_preview)
        misc_config = MiscConfig(self, css_config.reload_preview)

        self.pages.addWidget(md_config)
        self.pages.addWidget(css_config)
        self.pages.addWidget(misc_config)

        # add a save and a cancel button
        bottom_buttons = QtGui.QDialogButtonBox(
             QtGui.QDialogButtonBox.Save |  QtGui.QDialogButtonBox.Cancel
            )
        bottom_buttons.accepted.connect(self.save_and_close)
        bottom_buttons.rejected.connect(self.revert_and_close)

        self.create_icons()
        self.contents.setCurrentRow(ConfigurationDialog.OPEN_PAGE)
        self.contents.currentRowChanged.connect(self.change_page)

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
        self.pages.setCurrentIndex(ConfigurationDialog.OPEN_PAGE)
        self.exec_()

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
        markdown_button.setText(Configuration.USER_TEXT["markdown"])
        markdown_button.setTextAlignment(QtCore.Qt.AlignHCenter)
        markdown_button.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
            )

        css_button = QtGui.QListWidgetItem(self.contents)
        css_button.setIcon(
            QtGui.QIcon(Configuration.IMAGES["css"])
            )
        css_button.setText(Configuration.USER_TEXT["css"])
        css_button.setTextAlignment(QtCore.Qt.AlignHCenter)
        css_button.setFlags(
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


#==============================================================================
if (__name__ == "__main__"):
    pass
