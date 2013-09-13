#!/usr/bin/env python
# Written by: DGC

"""
This is a module for displaying information that there is a new version of the 
software.
"""

# python imports
from PyQt4 import QtGui, QtCore

# local imports
from UserText import USER_TEXT

#==============================================================================
def raise_new_version_dialog():
    """
    Raises the new version dialog
    """
    # global so it stays around without a parent
    global dialog
    dialog = NewVersionDialog()
    dialog.show()

#==============================================================================
class NewVersionDialog(QtGui.QMessageBox):
    """
    A dialog to tell the user that there is a new version, and where to get it.
    """
    def __init__(self):
        super(NewVersionDialog, self).__init__()
        self.setWindowTitle(USER_TEXT["update_available"])
        self.setText(USER_TEXT["update_message"])
        self.setTextFormat(QtCore.Qt.RichText);
        self.setIcon(QtGui.QMessageBox.Information)
        self.setStandardButtons(QtGui.QMessageBox.Close)

#==============================================================================
if (__name__ == "__main__"):
    pass
