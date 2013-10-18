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

import Configuration
import MarkdownEditor
import HiddenImports

#==============================================================================
def parse_args():
    """
    Gets the command line arguments and makes sense of them.
    """
    des = USER_TEXT["program_description"]
    parser = argparse.ArgumentParser(description=des)
    parser.add_argument(
        "files",
        metavar="file",
        help=USER_TEXT["file_argument"],
        nargs="*"
        )
    parser.add_argument(
        "-r",
        "--reset_user_conf",
        help=USER_TEXT["reset_user_conf_help"],
        action="store_true"
        )
    return parser.parse_args()

#==============================================================================
def main():
    """
    Parses the arguments, makes the app and editor
    """
    app = MarkdownEditor.MarkdownEditorApp(sys.argv)
    args = parse_args()
    logging.info("Program started with arguments: " + unicode(args))
    if (args.reset_user_conf):
        Configuration.reset_options()
    editor = MarkdownEditor.MarkdownEditor(args.files)
    sys.exit(app.exec_())

#==============================================================================
if (__name__ == "__main__"):
    main()
