#!/usr/bin/env python
# Written by: DGC

# python imports
from __future__ import unicode_literals

# local imports

#==============================================================================
class Document(object):
    
    def __init__(self, file_path):
        """
        If file_path is None this is a new file
        """
        self.file_path = file_path
        self.saved = (file_path is not None) 
        self.content = ""
        if (file_path):
            with open(self.file_path, "r") as markdown_file:
                self.content = markdown_file.read()

#==============================================================================
if (__name__ == "__main__"):
    pass
