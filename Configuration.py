#!/usr/bin/env python
# Written by: DGC

# python imports
from __future__ import unicode_literals

import collections
import getpass
import logging
import pickle
import os

# local imports
import Error
import Processor
import Resources
from UserText import USER_TEXT

#==============================================================================
def user_options_file_path():
    """
    Returns the path to the user specific options file
    Does not check if it exists.
    """
    # user environmental variable called different things on different systems
    name = "%s_Options.pickle" %(getpass.getuser())
    return os.path.join(Resources.directory(), name)

#==============================================================================
def default_options_file_path():
    """
    Returns the path to the default options file
    """
    # user environmental variable called different things on different systems
    return os.path.join(Resources.directory(), "Options.pickle")

#==============================================================================
def user_defined_word_list_path():
    """
    Returns the path to a personal word list file.
    """
    name = "%s.pwl" %(getpass.getuser())
    return os.path.join(Resources.directory(), name)
    
#==============================================================================
def language_directory():
    """
    Returns the Language directory.
    """
    return os.path.join(Resources.directory(), "Languages")
    
#==============================================================================
def read_options():
    filename = user_options_file_path()
    default_filename = default_options_file_path()
    if (not os.path.isfile(filename)):
        filename = default_filename
    with open(filename, "rb") as options_file:
        global OPTIONS
        OPTIONS = pickle.load(options_file)
    # for forward compatibility, if there are any new options add them to the
    # user specific ones
    with open(default_filename, "rb") as options_file:
        default_options = pickle.load(options_file)
    logging.info("Read options from %s", os.path.abspath(filename))
    for key in default_options:
        if (not key in OPTIONS):
            OPTIONS[key] = default_options[key]
            logging.warning(
                "Default option \"%s\" not in %s, read from %s instead",
                key, 
                os.path.abspath(filename), 
                os.path.abspath(default_filename)
                )

#==============================================================================
def save_options():
    options_path = user_options_file_path()
    with open(options_path, "wb") as options_file:
        pickle.dump(OPTIONS, options_file)
    logging.info("Options saved to %s", options_path)

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
        
        message = USER_TEXT["image_files_error"]
        image_dir = os.path.abspath(directory)
        detail =  USER_TEXT["image_files_error_detail"] %(image_dir)
        Error.show_error(message, detail, fatal=True)

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

#==============================================================================
def load_processor():
    global PROCESSOR
    PROCESSOR = PROCESSOR_TYPES[OPTIONS["processor"]](
        OPTIONS["display_line_numbers"],
        OPTIONS["code_css_class"],
        )

#==============================================================================
def reset_options():
    """
    Also deletes the user specific file.
    """
    filename = user_options_file_path()
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
    find_images()
    
    load_markdown_css()
    load_code_css()
    
    load_processor()

#==============================================================================
# Global variables and functions run on import
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

PROCESSOR_TYPES = collections.OrderedDict()
PROCESSOR_TYPES["markdown"] = Processor.Markdown
PROCESSOR_TYPES["markdown_extra"] = Processor.MarkdownExtra
PROCESSOR_TYPES["markdown_all"] = Processor.MarkdownAll
PROCESSOR_TYPES["codehilite"] = Processor.CodeHilite
PROCESSOR_TYPES["github_flavoured_markdown"] = Processor.GithubFlavouredMarkdown

on_import()

#==============================================================================
if (__name__ == "__main__"):
    pass
