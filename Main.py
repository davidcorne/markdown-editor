#!/usr/bin/env python
# Written by: DGC

# done before any other imports in case of errors in them

import Error
Error.set_exception_handler()

# python imports
import argparse
import sys

# local imports
from UserText import USER_TEXT

import Configuration
import MarkdownEditor
import HiddenImports
import Updater

#==============================================================================
def touch_files(files):
    """
    Will create each file in files if it does not already exist.
    if it cannot be created it will raise an error.
    """
    for markdown_file in files:
        try:
            open(markdown_file, "a").close()
        except IOError:
            Error.show_error(
                USER_TEXT["file_not_created"] %(markdown_file)
                )
            files.remove(markdown_file)

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
    parser.add_argument(
        "-c",
        "--create_files",
        help=USER_TEXT["create_file_option"],
        action="store_true",
        )
    return parser.parse_args()

#==============================================================================
def main():
    """
    Parses the arguments, makes the app and editor
    """
    app = MarkdownEditor.MarkdownEditorApp(sys.argv)
    args = parse_args()
    if (args.reset_user_conf):
        Configuration.reset_options()
    if (args.create_files):
        touch_files(args.files)
    editor = MarkdownEditor.MarkdownEditor(args.files)
    if (Updater.new_version_available()):
        Updater.raise_new_version_dialog(editor)
    sys.exit(app.exec_())

#==============================================================================
if (__name__ == "__main__"):
    main()
