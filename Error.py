#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import traceback

# local imports

from UserText import USER_TEXT

#==============================================================================
def exception_hook(exception_type, exception_value, trace):
    message = USER_TEXT["exception"]
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
    message_box.setWindowTitle(USER_TEXT["program_name"])
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
    tkMessageBox.showerror(
        USER_TEXT["program_name"],
        USER_TEXT["user_interface_import_fail"]
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
