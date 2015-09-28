#!/usr/bin/env python
# Written by: DGC

# python imports
import argparse
import logging
import sys

from PyQt4 import QtGui, QtCore

# local imports
import Localisation
import MarkdownEditor
import Configuration
import Updater
import UpdaterGui

from UserText import USER_TEXT
from ToolTips import TOOL_TIP

#==============================================================================
class MarkdownEditorApp(QtGui.QApplication):

    def __init__(self, command_args):
        super(MarkdownEditorApp, self).__init__(command_args)

        self.localisation = Localisation.Localiser()
        self.localisation.listeners.append(USER_TEXT)
        self.localisation.listeners.append(TOOL_TIP)
        self.localisation.listeners.append(self)

        logging.info("Localisation setup.")
        logging.info(
            "Application started with arguments: " + unicode(command_args)
            )
        args = self.parse_command_args(command_args[1:])
        if (args.reset_user_conf):
            Configuration.reset_options()
        self.language_changed(self.localisation.language())


        if (args.locale):
            self.localisation.set_language(args.locale)
        self.setWindowIcon(QtGui.QIcon(Configuration.IMAGES["icon"]))
        self.editor = MarkdownEditor.MarkdownEditor(
            args.files, 
            self.localisation
        )

        if (args.command):
            input_file = args.command[0]
            output_file = args.command[1]
            CommandLineMarkdownApp(input_file, output_file).run()
            self.editor.hide()
            sys.exit()

        logging.info("Updater checking for updates.")
        self.updater = Updater.Updater()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check_update_finished)
        self.timer.start(50)

    def language_changed(self, locale):
        QtCore.QLocale.setDefault(QtCore.QLocale(locale))

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
        parser.add_argument(
            "-l",
            "--locale",
            help=USER_TEXT["set_locale"]
        )
        parser.add_argument(
            "-cmd",
            "--command",
            nargs=2,
            metavar=(
                USER_TEXT["command_line_mode_input"],
                USER_TEXT["command_line_mode_output"]
            ),
            help=USER_TEXT["command_line_mode"]
        )
        return parser.parse_args(args)
        
    def check_update_finished(self):
        if (self.updater.finished):
            logging.info("Updater finished checking for updates.")
            if (self.updater.update_available):
                logging.info("Update available.")
                UpdaterGui.raise_new_version_dialog()
            self.timer.stop()

    def __del__(self):
        self.localisation.listeners.remove(self)
        super(MarkdownEditorApp, self).__del__()

#==============================================================================
class CommandLineMarkdownApp(object):
    """
    This deals with the command line application concerns.
    """
    
    def __init__(self, input_file, output_file):
        logging.info("Command line application started.")
        import Error
        Error.reset_exception_handler()
        self.input_file = input_file
        self.output_file = output_file

    def run(self):
        with open(self.input_file, "r") as markdown_file:
            text = markdown_file.read()
        html = MarkdownEditor.process_markdown(text)
        with open(self.output_file, "w") as html_file:
            html_file.write(html)
        logging.info("Markdown in {0} converted and written to {1}".format(
            self.input_file,
            self.output_file
        ))

#==============================================================================
if (__name__ == "__main__"):
    pass
