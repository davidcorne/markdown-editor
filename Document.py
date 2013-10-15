#!/usr/bin/env python
# Written by: DGC

# python imports
from __future__ import unicode_literals

import os

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

    @property
    def filename(self):
        if (self.file_path is not None):
            return os.path.basename(unicode(self.file_path))

    def save_file(self):
        with open(self.file_path, "w") as text_file:
            text_file.write(self.content)
        self.saved = True

    def colour(self, beginning, end):
        pass

    def bold(self, beginning, end):
        pass

    def italic(self, beginning, end):
        pass

    def code(self, beginning, end):
        pass

    def insert_link(self, beginning, end):
        pass

#==============================================================================
if (__name__ == "__main__"):
    pass
