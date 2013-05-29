#!/usr/bin/env python
# Written by: DGC
#
#D This is purely for developer use, it will not be included in the program it 
#D is just for adding/changing options in the standard Options.pickle file.
#

# python imports
from __future__ import unicode_literals

import os
import pickle
import sys

# local imports

OPTIONS = {
    "code_css": "Standard", 
    "show_html": False,
    "processor": "github_flavoured_markdown",
    "markdown_css": "Markdown"
    }

#==============================================================================
def write_options_file():
    options_path = os.path.join(
        os.path.dirname(sys.argv[0]),
        "../Resources/Options.pickle"
        )
    with open(options_path, "wb") as options_file:
        pickle.dump(OPTIONS, options_file)
    
#==============================================================================
if (__name__ == "__main__"):
    write_options_file()
