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

#==============================================================================
def save_options():
    options_path = os.path.join(resource_dir(), options_file_name())
    with open(options_path, "wb") as options_file:
        pickle.dump(OPTIONS, options_file)
    
#==============================================================================
def read_user_text():
    filename = os.path.join(resource_dir(), "UserText.pickle")
    with open(filename, "rb") as user_text_file:
        global USER_TEXT
        USER_TEXT = pickle.load(user_text_file)

#==============================================================================
def read_tool_tips():
    filename = os.path.join(resource_dir(), "ToolTips.pickle")
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
    directory = os.path.join(resource_dir(), "Images")
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

read_options()
read_user_text()
read_tool_tips()
find_images()

reload_markdown_css()
reload_code_css()

PROCESSOR_TYPES = collections.OrderedDict()
PROCESSOR_TYPES["markdown"] = Processor.Markdown
PROCESSOR_TYPES["markdown_extra"] = Processor.MarkdownExtra
PROCESSOR_TYPES["github_flavoured_markdown"] = Processor.GithubFlavouredMarkdown

PROCESSOR = PROCESSOR_TYPES[OPTIONS["processor"]]()

#==============================================================================
if (__name__ == "__main__"):
    pass
