#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import traceback

# local imports
import Resources

#==============================================================================
def get_user_text():
    """
    This is done here in case the user text file is not found.
    """
    try:
        from UserText import USER_TEXT
    except IOError:
        # The user text file has not been found, this is doing quite a lot in
        # an except block, but this SHOULD be safe.
        USER_TEXT = {
            "exception": """\
There has been an installation error.

Cannot find localisation file:
  %s

Please report this at https://bitbucket.org/davidcorne/markdown-editor/issues

Sorry for any inconvenience.
""" %(Resources.directory()),
            "program_name": "MarkdownEditor",
            }
    return USER_TEXT

#==============================================================================
def exception_hook(exception_type, exception_value, trace):
    message = get_user_text()["exception"]
    detail = traceback.format_exception(
        exception_type,
        exception_value,
        trace
        )
    detail = "".join(detail)
    show_error(message, detail)

#==============================================================================
def show_error(message, detail=None):
    try:
        from PyQt4 import QtGui
    except ImportError:
        tk_quit()
    if (not QtGui.QApplication.instance()):
        app = QtGui.QApplication(sys.argv)
    message_box = QtGui.QMessageBox()
    message_box.setWindowTitle(get_user_text()["program_name"])
    message_box.setIcon(QtGui.QMessageBox.Critical)
    message_box.addButton(QtGui.QMessageBox.Ok)
    message_box.setText(message)
    if (detail):
        message_box.setDetailedText(detail)
    message_box.exec_()

#==============================================================================
def tk_quit():
    """
    The only reason you should get here is an import error from Qt.
    """
    import tkMessageBox
    user_text = get_user_text()
    tkMessageBox.showerror(
        user_text["program_name"],
        user_text["user_interface_import_fail"]
        )
    sys.exit()

#==============================================================================
def set_exception_handler():
    sys.excepthook = exception_hook

#==============================================================================
def reset_exception_handler():
    sys.excepthook = sys.__excepthook__

#==============================================================================
if (__name__ == "__main__"):
    pass
