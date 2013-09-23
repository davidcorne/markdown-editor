#!/usr/bin/env python
# Written by: DGC

"""
This is a module to convert an image to bytes so it can be embedded in html 
rather than linked.
"""
# python imports
import os
import base64

# local imports
import html

#==============================================================================
def image_to_base_64_bytes(path):
    """
    This takes a path and returns a byte array from the image. This byte array
    is base 64

    Exceptions:
      IOError if the path does not exist.

    """
    with open(path, "rb") as image:
        data = base64.standard_b64encode(image.read())
    return data

#==============================================================================
def path_to_image_tag(path, alt="", title=""):
    """
    This takes a path and returns a byte array from the image. This byte array
    is base 64
    
    Exceptions:
      IOError if the path does not exist.
    
    """
    #img = [
    #    "<img ",
    #    "alt=\"",
    #    alt,
    #    "\" ",
    #    "src=\"",
    #    "data:image;base64,",
    #    image_to_base_64_bytes(path),
    #    "\" ",
    #    "title=\"",
    #    title,
    #    "\"",
    #    "/>"
    #    ]
    img = html.Node("img")
    img["title"] = title
    img["alt"] = alt
    img["src"] = "data:image;base64,%s" %(image_to_base_64_bytes(path))
    return img.to_string()

#==============================================================================
if (__name__ == "__main__"):
    """
    Print an image tag for any images given as arguments.
    """
    import sys
    for path in sys.argv[1:]:
        print(path_to_image_tag(path))
        print("")
