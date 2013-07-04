#!/usr/bin/env python
# Written by: DGC

"""
In some extensions there are from . import * or similar which pyinstaller can't
work out, so manually import them here.
"""
# python imports

# import all the extensions which are "hidden" to pyinstaller
import markdown.extensions.extra
import markdown.extensions.codehilite
import markdown.extensions.abbr
import markdown.extensions.attr_list
import markdown.extensions.def_list
import markdown.extensions.fenced_code
import markdown.extensions.footnotes
import markdown.extensions.tables
import markdown.extensions.smart_strong

# hidden imports from pygments
import pygments.lexers.parsers
import pygments.lexers.math
import pygments.lexers.asm
import pygments.lexers.templates
import pygments.lexers.foxpro
import pygments.lexers.special
import pygments.lexers.dalvik
import pygments.lexers.hdl

# local imports

#==============================================================================
if (__name__ == "__main__"):
    pass
