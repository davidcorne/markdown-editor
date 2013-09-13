#!/usr/bin/env python
# Written by: DGC

"""
This is a module for checking if there is a new version of the software and
has view classes to notify the user.
"""

# python imports

from PyQt4 import QtGui, QtCore

# local imports

from UserText import USER_TEXT
from ToolTips import TOOL_TIP

USER_TEXT["update_available"] = "Update Available"
USER_TEXT["update_message"] = """\
There is an update available to download from the <a href="https://bitbucket.org/davidcorne/markdown-editor-downloads/src/tip/setup.exe?at=default">download site</a>
"""

#==============================================================================
def new_version_available():
    """
    Checks this version and checks the download site for a new version.
    """
    return True

#==============================================================================
def current_version():
    """
    Returns the version of the software being run.
    """
    pass

#==============================================================================
def available_version():
    """
    Returns the version available to download.
    """
    pass

#==============================================================================
def raise_new_version_dialog(parent):
    """
    Raises the new version dialog
    """
    dialog = NewVersionDialog(parent)
    dialog.show()

#==============================================================================
class NewVersionDialog(QtGui.QMessageBox):
    """
    A dialog to tell the user that there is a new version, and where to get it.
    """
    def __init__(self, parent):
        super(NewVersionDialog, self).__init__(parent)
        self.setWindowTitle(USER_TEXT["update_available"])
        self.setText(USER_TEXT["update_message"])
        self.setTextFormat(QtCore.Qt.RichText);
        self.setIcon(QtGui.QMessageBox.Information)
        self.setStandardButtons(QtGui.QMessageBox.Close)

#==============================================================================
if (__name__ == "__main__"):
    pass
