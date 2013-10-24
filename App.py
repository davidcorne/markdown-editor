#!/usr/bin/env python
# Written by: DGC

# python imports
import argparse
import logging

from PyQt4 import QtGui, QtCore

# local imports
import MarkdownEditor
import Configuration
import Updater

from UserText import USER_TEXT

#==============================================================================
class MarkdownEditorApp(QtGui.QApplication):

    def __init__(self, command_args):
        super(MarkdownEditorApp, self).__init__(command_args)

        logging.info(
            "Application started with arguments: " + unicode(command_args)
            )
        args = self.parse_command_args(command_args[1:])
        if (args.reset_user_conf):
            Configuration.reset_options()

        self.setWindowIcon(QtGui.QIcon(Configuration.IMAGES["icon"]))
        self.editor = MarkdownEditor.MarkdownEditor(args.files)

        logging.info("Updater checking for updates.")
        self.updater = Updater.Updater()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check_update_finished)
        self.timer.start(50)

    def parse_command_args(self, args):
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
        return parser.parse_args(args)
        
    def check_update_finished(self):
        if (self.updater.finished):
            logging.info("Updater finished checking for updates.")
            if (self.updater.update_available):
                logging.info("Update available.")
                UpdaterGui.raise_new_version_dialog()
            self.timer.stop()

#==============================================================================
if (__name__ == "__main__"):
    pass
