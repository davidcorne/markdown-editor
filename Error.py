#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import traceback

# local imports

#==============================================================================
def get_user_text():
    """
    This gets the user text so we don't have to import Configuration at the 
    top of the file. This means ANY error can be shown in a window, including 
    import errors.
    """
    try:
        import Configuration
        user_text = Configuration.USER_TEXT
    # Not good to catch all exceptions, but this is for safety the import
    # could have failed or a file might not be there, anything could happen
    except :
        user_text = {
            # we know if this fails, the installation is wrong.
            "exception": "An installation error has occured.",
            "program_name": "MarkdownEditor",
            }
    return user_text
    
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
    The only reason you shouldd get here is an import error.
    """
    import tkMessageBox
    message = """\
User interface library not loaded.

Please report this at https://bitbucket.org/davidcorne/markdown-editor/issues
"""
    tkMessageBox.showerror(
        get_user_text()["program_name"],
        message
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
