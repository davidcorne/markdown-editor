#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import traceback

from PyQt4 import QtGui

# local imports
import Configuration

#==============================================================================
def exception_hook(exception_type, exception_value, trace):
    message = Configuration.USER_TEXT["exception"]
    detail = traceback.format_exception(
        exception_type,
        exception_value,
        trace
        )
    detail = "".join(detail)
    show_error(message, detail)

#==============================================================================
def show_error(message, detail=None):
    if (not QtGui.QApplication.instance()):
        app = QtGui.QApplication(sys.argv)
    message_box = QtGui.QMessageBox()
    message_box.setWindowTitle(Configuration.USER_TEXT["program_name"])
    message_box.setIcon(QtGui.QMessageBox.Critical)
    message_box.addButton(QtGui.QMessageBox.Ok)
    message_box.setText(message)
    if (detail):
        message_box.setDetailedText(detail)
    message_box.exec_()

#==============================================================================
def set_exception_handler():
    sys.excepthook = exception_hook

#==============================================================================
def reset_exception_handler():
    sys.excepthook = sys.__excepthook__

#==============================================================================
if (__name__ == "__main__"):
    pass
