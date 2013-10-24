#!/usr/bin/env python
# Written by: DGC

# python imports
from PyQt4 import QtGui

# local imports
import Configuration

from UserText import USER_TEXT

#==============================================================================
class ImageDialog(QtGui.QDialog):

    def __init__(self, parent, window_title):
        super(ImageDialog, self).__init__(parent)
        
        self.accepted = False

        self.initialise_ui()
        self.setWindowTitle(window_title)

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

    def browse_for_image(self):
        file_path = QtGui.QFileDialog.getOpenFileName(
            self,
            USER_TEXT["browse_for_image"],
            self.parentWidget().editor.current_directory(),
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
class LinkImageDialog(ImageDialog):

    def __init__(self, parent):
        super(LinkImageDialog, self).__init__(parent, USER_TEXT["link_image"])

#==============================================================================
class EmbedImageDialog(ImageDialog):

    def __init__(self, parent):
        super(EmbedImageDialog, self).__init__(
            parent, 
            USER_TEXT["embed_image"]
            )

#==============================================================================
if (__name__ == "__main__"):
    pass
