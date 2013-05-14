#!/usr/bin/env python
# Written by: DGC

# python imports
import os
import sys

# local imports
import Error

OPTIONS = {
    "Show html": False,
    }

MARKDOWN_FILE_STRING = """\
Markdown (*.md *.markdown *.mdown *.mkdn *.mkd *.mdtxt *.mdtext *.text);;\
All Files (*)\
"""

USER_TEXT = {
    "program_name": "MarkdownEditor",
    "undo_redo_toolbar": "Undo Redo Toolbar",
    "format_toolbar": "Format Toolbar",
    "file_toolbar": "File Toolbar",
    "edit_toolbar": "Edit Toolbar",
    "edit_menu": "&Edit",
    "tools_menu": "&Tools",
    "file_menu": "&File",
    "find_what": "Find &what:",
    "match_case": "Match &case",
    "match_whole_words": "Match &whole words",
    "search_backwards": "Search &backwards",
    "find_title": "Find",
    "find": "&Find",
    "close": "Close",
    "configuration": "Configuration",
    "close_file": "Close File",
    "configure": "Configure",
    "copy" : "Copy",
    "cut" : "Cut",
    "paste" : "Paste",
    "export_html" : "Export html",
    "new_file" : "New File",
    "open_file" : "Open File",
    "undo" : "Undo",
    "redo" : "Redo",
    "save_file" : "Save",
    "save_all" : "Save All Files",
    "save_as" : "Save As",
    "find_and_replace" : "Find and Replace",
    "select_all" : "Select All",
    "saved": "File saved",
    "exception" : "An internal error has occured.",
    "error_text_was": "The text from it was:",
    }

TOOL_TIP = {
    "bold": "Surround the highlighted area with strong emphasis (__)",
    "italic": "Surround the highlighted area with emphasis (_)",
    "code": "Surround the highlighted area with code blocks (```)",
    "choose_colour": "Raise a colour chooser dialog",
    "close_file": "Close the currently open document",
    "configure": "Configure the program",
    "copy": "Copy the highlighted area to the clipboard",
    "cut": "Cut the highlighted area to the clipboard",
    "export_html": "Export the current document as html",
    "find_and_replace": "Raise the find and replace window",
    "new_file": "Start a new document",
    "open_file": "Open an existing document",
    "paste": "Paste from the clipboard to the current cursor location",
    "redo": "Redo the previous undo",
    "save_all": "Save all open documents",
    "save_as": "Save the current document with a specified name",
    "save_file": "Save the current document",
    "select_all": "Select all the text in the current document",
    "set_colour": "Set the colour of the highlighted area to this colour",
    "undo": "Undo the previous change",
    }

#==============================================================================
class Images(object):

    def __init__(self):
        self.images = dict()

    def __getitem__(self, key):
        if (not self.images):
            self.find_images()
        return self.images[key]

    def find_images(self):
        directory = os.path.join(os.path.dirname(sys.argv[0]), "Images")
        if (os.path.isdir(directory)):
            for image in os.listdir(directory):
                self.images[os.path.splitext(image)[0]] = os.path.join(
                    directory, 
                    image
                    )
        else:
            message = ["Images not found at location:", "\n\n", directory]
            message = "".join(message)
            Error.show_error(message)


def find_images():
    directory = os.path.join(os.path.dirname(sys.argv[0]), "Images")
    if (os.path.isdir(directory)):
        for image in os.listdir(directory):
            self.images[os.path.splitext(image)[0]] = os.path.join(
                directory, 
                image
                )
    else:
        message = ["Images not found at location:", "\n\n", directory]
        message = "".join(message)
        Error.show_error(message)

#IMAGES = Images()
IMAGES = find_images()
    
#==============================================================================
if (__name__ == "__main__"):
    pass
