#!/usr/bin/env python
# Written by: DGC

# done before any other imports in case of errors in them

import Error
Error.set_exception_handler()

# python imports
import argparse
import logging
import sys

# local imports
from UserText import USER_TEXT

import App
import HiddenImports
import Log

#==============================================================================
def main():
    Log.start_logging()
    app = run(sys.argv)
    sys.exitfunc = lambda : logging.info("Program exited.")
    sys.exit(app.exec_())

#==============================================================================
def run(arguments):
    """
    Parses the arguments, makes the app and editor. Returns the app.
    """
    app = App.MarkdownEditorApp(arguments)
    return app

#==============================================================================
if (__name__ == "__main__"):
    main()
