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
    message = list(Configuration.USER_TEXT["exception"])
    if (exception_value.message):
        message.append(" ")
        message.append(Configuration.USER_TEXT["error_text_was"])
        message.append("\n\n")
        message.append(exception_value.message)
    message = "".join(message)
    trace = "".join(traceback.format_tb(trace))
    show_error(message, trace)

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


def set_exception_handler():
    sys.excepthook = exception_hook

#==============================================================================
if (__name__ == "__main__"):
    pass
