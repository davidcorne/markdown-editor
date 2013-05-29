#!/usr/bin/env python
# Written by: DGC

# python imports
from __future__ import unicode_literals

import collections
import pickle
import os
import sys

# local imports
import Error
import Processor

#==============================================================================
def resource_dir():
    """
    Returns the directory this is being run from.
    """
    return os.path.join(os.path.dirname(sys.argv[0]), "Resources")

#==============================================================================
def options_file_name():
    # user environmental variable called different things on different systems
    name = "_Options.pickle"
    if (os.environ.get("USER")):
        name = os.environ.get("USER") + name
    elif (os.environ.get("USERNAME")):
        name = os.environ.get("USERNAME") + name
    return name

#==============================================================================
def read_options():
    filename = os.path.join(resource_dir(), options_file_name())
    if (not os.path.isfile(filename)):
        filename = os.path.join(resource_dir(), "Options.pickle")
    with open(filename, "rb") as options_file:
        global OPTIONS
        OPTIONS = pickle.load(options_file)

read_options()

#==============================================================================
def save_options():
    options_path = os.path.join(resource_dir(), options_file_name())
    with open(options_path, "wb") as options_file:
        pickle.dump(OPTIONS, options_file)
    
MARKDOWN_FILE_STRING = """\
Markdown (*.md *.markdown *.mdown *.mkdn *.mkd *.mdtxt *.mdtext *.text);;\
All Files (*)\
"""

# full image formats from list in MS word dropdown - probably overkill
IMAGE_FILE_STRING = """\
Images (*.png *.jpg *.jpeg *.gif *.bmp *.emf *.wmf *.jfif *.jpe *.dib *.rle \
*.bmz *.gfa *.emz *.wmz *.pcz *.tif *.tiff *.cgm *.eps *.pct *.pict *.wpg);;\
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
    "replace_title": "Replace",
    "replace_with": "Replace with:",
    "replace": "&Replace",
    "replace_all": "Replace &all",
    "find": "&Find",
    "close": "Close",
    "close_file": "Close File",
    "options": "Options",
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
    "insert_link": "Insert Link",
    "enter_link": "Enter the destination URL",
    "insert_image": "Insert Image",
    "enter_image_location": "Enter the image location",
    "enter_image_title": "Enter the image title (optional)",
    "browse_for_image": "Browse for image",
    "current_document": "the current document",
    "save_changes?": "Do you want to save your changes?",
    "made_changes": "You have made changes to",
    "markdown": "Markdown",
    "markdown_extra": "Markdown Extra",
    "github_flavoured_markdown": "Github Flavoured Markdown",
    "show_html": "Show HTML",
    "misc": "Miscellaneous",
    "markdown_type": "Markdown Type",
    "debug_options": "Debug Options",
    "css": "CSS",
    "style_name": "Style Name",
    "code": "Code",
    "preview": "Preview",
    "print": "Print",
    "print_markdown": "Print Markdown",
    "print_rendered_html": "Print Rendered HTML",
    "print_raw_html": "Print Raw HTML Code",
    "print_preview_markdown": "Print Preview Markdown",
    "print_preview_rendered_html": "Print Preview Rendered HTML",
    "print_preview_raw_html": "Print Preview Raw HTML Code",
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
    "link": "Insert a link with the link text of the surrounded area",
    "image": "Insert an image with the title of the surrounded area",
    "print_menu": "Opens the printing menu",
    "print_markdown": "Prints the markdown document",
    "print_rendered_html": "Prints the HTML output as it will be rendered by a browser",
    "print_raw_html": "Prints the raw HTML code output",
    "print_preview_markdown": "Shows a preview of the markdown before printing",
    "print_preview_rendered_html": "Shows a preview of the HTML output as it will be rendered by a browser before printing",
    "print_preview_raw_html": "Shows a preview of the raw HTML code output before printing",
    }

#==============================================================================
def find_images():
    images = dict()
    directory = os.path.join(resource_dir(), "Images")
    if (os.path.isdir(directory)):
        for image in os.listdir(directory):
            images[os.path.splitext(image)[0]] = os.path.join(
                directory, 
                image
                )
    else:
        message = "Image files not found."
        detail = "Images should be found at " + os.path.abspath(directory)
        Error.show_error(message, detail)
    return images

IMAGES = find_images()

PROCESSOR_TYPES = collections.OrderedDict()
PROCESSOR_TYPES["markdown"] = Processor.Markdown
PROCESSOR_TYPES["markdown_extra"] = Processor.MarkdownExtra
PROCESSOR_TYPES["github_flavoured_markdown"] = Processor.GithubFlavouredMarkdown

PROCESSOR = PROCESSOR_TYPES[OPTIONS["processor"]]()

#==============================================================================
def read_css(filename):
    filename += ".css"
    directory = os.path.join(resource_dir(), "CSS")
    filename = os.path.join(directory, filename)
    with open(filename, "r") as css_file:
        return css_file.read()

#==============================================================================
def reload_markdown_css():
    css = ""
    if (OPTIONS["markdown_css"]):
        css = read_css("Markdown/" + OPTIONS["markdown_css"])
    global MARKDOWN_CSS
    MARKDOWN_CSS = css

#==============================================================================
def reload_code_css():
    css = ""
    if (OPTIONS["code_css"]):
        css = read_css("Code/" + OPTIONS["code_css"])
    global CODE_CSS
    CODE_CSS = css

reload_markdown_css()
reload_code_css()

#==============================================================================
if (__name__ == "__main__"):
    pass
