#!/usr/bin/env python
# Written by: DGC
#
#D This is purely for developer use, it will not be included in the program it 
#D is just for adding/changing options in the standard Options.pickle file.
#

# python imports
from __future__ import unicode_literals

import os
import csv
import pickle
import sys

# local imports

OPTIONS = {
    "code_css": "Standard", 
    "code_css_class": "highlight",
    "show_html": False,
    "processor": "markdown_all",
    "markdown_css": "Markdown",
    "display_line_numbers": False,
    "font": "Arial,12,-1,5,50,0,0,0,0,0",
    }

LOCALISATION_OPTIONS = {
    "language": "en_GB",
    "available_languages": ["en_GB", "de_DE", "en_AU", "en_US", "fr_FR"],
}

TEST_OPTIONS = {
    "code_css": "", 
    "code_css_class": "highlight",
    "show_html": False,
    "processor": "markdown_all",
    "markdown_css": "",
    "display_line_numbers": False,
    "font": "Arial,12,-1,5,50,0,0,0,0,0",
#    "language": "en_GB",
}

USER_TEXT_KEYS = [
    "program_name",
    "undo_redo_toolbar",
    "format_toolbar",
    "file_toolbar",
    "edit_toolbar",
    "edit_menu",
    "tools_menu",
    "file_menu",
    "find_what",
    "match_case",
    "match_whole_words",
    "search_backwards",
    "find_title",
    "replace_title",
    "replace_with",
    "replace",
    "replace_all",
    "find",
    "close",
    "close_file",
    "options",
    "copy" ,
    "cut" ,
    "paste" ,
    "export_html" ,
    "export_pdf" ,
    "new_file" ,
    "open_file" ,
    "undo" ,
    "redo" ,
    "save_file" ,
    "save_all" ,
    "save_as" ,
    "find_and_replace" ,
    "select_all" ,
    "saved",
    "exception" ,
    "insert_link",
    "enter_link",
    "link_image",
    "embed_image",
    "enter_image_location",
    "image_location",
    "enter_image_title",
    "browse_for_image",
    "current_document",
    "save_changes?",
    "made_changes",
    "markdown",
    "markdown_extra",
    "markdown_all",
    "codehilite",
    "github_flavoured_markdown",
    "show_html",
    "misc",
    "markdown_type",
    "debug_options",
    "css",
    "style_name",
    "code",
    "preview",
    "print",
    "print_markdown",
    "print_rendered_html",
    "print_raw_html",
    "print_preview_markdown",
    "print_preview_rendered_html",
    "print_preview_raw_html",
    "show_line_numbers",
    "other_options",
    "help_menu",
    "help_link",
    "display_options",
    "set_font",
    "change_font",
    "user_interface_import_fail",
    "image_files_error",
    "image_files_error_detail",
    "code_css_class",
    "program_description",
    "reset_user_conf_help",
    "file_argument",
    "create_file_option",
    "file_not_found",
    "file_not_created",
    "update_available",
    "update_message",
    "logging_file_location",
    "log_file_location",
    "add_to_dictionary",
]

TOOL_TIPS_KEYS = [
    "bold",
    "italic",
    "code",
    "choose_colour",
    "close_file",
    "configure",
    "copy",
    "cut",
    "export_html",
    "export_pdf",
    "find_and_replace",
    "new_file",
    "open_file",
    "paste",
    "redo",
    "save_all",
    "save_as",
    "save_file",
    "select_all",
    "set_colour",
    "undo",
    "link",
    "link_image",
    "embed_image",
    "image_menu",
    "print_menu",
    "print_markdown",
    "print_rendered_html",
    "print_raw_html",
    "print_preview_markdown",
    "print_preview_rendered_html",
    "print_preview_raw_html",
    "help_link",
    "show_log_file_location",
]

#==============================================================================
def write_config_file(object, file_name, directory="Resources"):
    """
    Pickles the object to file_name where file_name is a relative path under 
    Resources
    """
    options_path = os.path.join(
        os.path.dirname(sys.argv[0]),
        "../" + directory
        )
    file_path = os.path.join(options_path, file_name)
    with open(file_path, "wb") as options_file:
        pickle.dump(object, options_file)

#==============================================================================
def write_options_files():
    write_config_file(OPTIONS, "Options.pickle")
    write_config_file(
        LOCALISATION_OPTIONS, 
        "Languages.pickle", 
        directory="Resources/Languages"
    )
    write_config_file(TEST_OPTIONS, "Options.pickle", directory="Integration")
    
#==============================================================================
def write_user_strings(file_name, verifier):
    with open("data/" + file_name + ".csv", "rb") as csvfile:
        table = csv.reader(csvfile)
        for i, row in enumerate(table):
            if (i == 0):
                keys = row[1:]
                for verifier_key in verifier:
                    if not verifier_key in keys:
                        raise Exception(
                            "%s not in %s keys" %(verifier_key, file_name)
                        )
                continue
            language = row[0]
            user_text = dict(zip(keys, row[1:]))
            write_config_file(
                user_text,
                file_name + ".pickle", 
                directory="Resources/Languages/" + language)
    
#==============================================================================
def write_user_text():
    write_user_strings("UserText", USER_TEXT_KEYS)

#==============================================================================
def write_tool_tips():
    write_user_strings("ToolTips", TOOL_TIPS_KEYS)
    
#==============================================================================
if (__name__ == "__main__"):
    write_options_files()
    write_user_text()
    write_tool_tips()
