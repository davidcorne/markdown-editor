#!/usr/bin/env python
# Written by: DGC

# python imports
import os
import sys

# local imports

OPTIONS = {
    "Show html": False,
    }

MARKDOWN_FILE_STRING = """\
Markdown (*.md *.markdown *.mdown *.mkdn *.mkd *.mdtxt *.mdtext *.text);;\
All Files (*)\
"""

#==============================================================================
def find_images():
    images = dict()
    directory = os.path.join(os.path.dirname(sys.argv[0]), "Images")
    for image in os.listdir(directory):
        images[os.path.splitext(image)[0]] = os.path.join(directory, image)
    return images

IMAGES = find_images()
    
#==============================================================================
if (__name__ == "__main__"):
    pass
