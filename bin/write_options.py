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
import re

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
def verify_keys(file_name, keys, verifier):
    keys = set(keys)
    verifier = set(verifier)
    difference = [k for k in keys if k not in verifier]
    if (difference):
        raise Exception(
            "Bad key found in %s: %s" %(file_name, str(difference))
        )
    
#==============================================================================
def write_user_strings(file_name, verifier):
    with open("data/" + file_name + ".csv", "rb") as csvfile:
        table = csv.reader(csvfile)
        for i, row in enumerate(table):
            if (i == 0):
                keys = row[1:]
                verify_keys(file_name, keys, verifier)
                continue
            language = row[0]
            user_text = dict(zip(keys, row[1:]))
            write_config_file(
                user_text,
                file_name + ".pickle", 
                directory="Resources/Languages/" + language)

#==============================================================================
def generate_keys(pattern):
    keys = list()
    for path in os.listdir("."):
        if (path[-3:] == ".py"):
            with open(path, "r") as py_file:
                lines = py_file.readlines()
            for line in lines:
                if (pattern.lower() in line.lower()):
                    match = re.search(".*" + pattern + "\[\"(.*)\"\]", line)
                    if match:
                        keys.append(match.group(1))
    return keys

#==============================================================================
def generate_user_text_keys():    
    return generate_keys("USER_TEXT")
                    
#==============================================================================
def generate_tool_tips_keys():    
    return generate_keys("TOOL_TIP")
                    
#==============================================================================
def write_user_text():
    write_user_strings("UserText", generate_user_text_keys())

#==============================================================================
def write_tool_tips():
    write_user_strings("ToolTips", generate_tool_tips_keys())
    
#==============================================================================
if (__name__ == "__main__"):
    write_options_files()
    write_user_text()
    write_tool_tips()
