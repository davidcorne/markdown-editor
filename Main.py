#!/usr/bin/env python
# Written by: DGC

# before everything else, setup
import SetupEnv

# python imports
import logging
import sys

# local imports
import App

#==============================================================================
def main():
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
