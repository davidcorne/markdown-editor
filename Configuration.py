#!/usr/bin/env python
# Written by: DGC

# python imports
from __future__ import unicode_literals

import collections
import pickle
import os

# local imports
import Error
import Processor
import Resources

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
    filename = os.path.join(Resources.directory(), options_file_name())
    default_filename = os.path.join(Resources.directory(), "Options.pickle")
    if (not os.path.isfile(filename)):
        filename = default_filename
    with open(filename, "rb") as options_file:
        global OPTIONS
        OPTIONS = pickle.load(options_file)
    # for forward compatibility, if there are any new options add them to the
    # user specific ones
    with open(default_filename, "rb") as options_file:
        default_options = pickle.load(options_file)
    for key in default_options:
        if (not key in OPTIONS):
            OPTIONS[key] = default_options[key]

#==============================================================================
def save_options():
    options_path = os.path.join(Resources.directory(), options_file_name())
    with open(options_path, "wb") as options_file:
        pickle.dump(OPTIONS, options_file)
    
#==============================================================================
def read_tool_tips():
    filename = os.path.join(Resources.directory(), "ToolTips.pickle")
    with open(filename, "rb") as tool_tips_file:
        global TOOL_TIP
        TOOL_TIP = pickle.load(tool_tips_file)

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

#==============================================================================
def find_images():
    global IMAGES
    IMAGES = dict()
    directory = os.path.join(Resources.directory(), "Images")
    if (os.path.isdir(directory)):
        for image in os.listdir(directory):
            IMAGES[os.path.splitext(image)[0]] = os.path.join(
                directory, 
                image
                )
    else:
        message = "Image files not found."
        detail = "Images should be found at " + os.path.abspath(directory)
        Error.show_error(message, detail)

#==============================================================================
def read_css(directory, filename):
    filename += ".css"
    css_directory = os.path.join(Resources.directory(), "CSS")
    directory = os.path.join(css_directory, directory)
    path = os.path.join(directory, filename)
    if (not os.path.isfile(path)):
        user_directory = os.path.join(directory, "User")
        path = os.path.join(user_directory, filename)
    with open(path, "r") as css_file:
        return css_file.read()

#==============================================================================
def load_markdown_css():
    css = ""
    if (OPTIONS["markdown_css"]):
        css = read_css("Markdown", OPTIONS["markdown_css"])
    global MARKDOWN_CSS
    MARKDOWN_CSS = css

#==============================================================================
def load_code_css():
    css = ""
    if (OPTIONS["code_css"]):
        css = read_css("Code", OPTIONS["code_css"])
    global CODE_CSS
    CODE_CSS = css



PROCESSOR_TYPES = collections.OrderedDict()
PROCESSOR_TYPES["markdown"] = Processor.Markdown
PROCESSOR_TYPES["markdown_extra"] = Processor.MarkdownExtra
PROCESSOR_TYPES["markdown_all"] = Processor.MarkdownAll
PROCESSOR_TYPES["codehilite"] = Processor.CodeHilite
PROCESSOR_TYPES["github_flavoured_markdown"] = Processor.GithubFlavouredMarkdown

#==============================================================================
def load_processor():
    global PROCESSOR
    PROCESSOR = PROCESSOR_TYPES[OPTIONS["processor"]]()


#==============================================================================
def reset_options():
    """
    Also deletes the user specific file.
    """
    filename = os.path.join(Resources.directory(), options_file_name())
    if (os.path.isfile(filename)):
        os.remove(filename)
    read_options()
    load_processor()

#==============================================================================
def on_import():
    """
    Makes all the global config options.
    """
    read_options()
    read_tool_tips()
    find_images()
    
    load_markdown_css()
    load_code_css()
    
    load_processor()

on_import()

#==============================================================================
if (__name__ == "__main__"):
    pass
