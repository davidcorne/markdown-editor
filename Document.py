#!/usr/bin/env python
# Written by: DGC

# python imports

# local imports

#==============================================================================
class Document(object):
    
    def __init__(self, file_path):
        """
        If file_path is None this is a new file
        """
        self.file_path = file_path
        self.saved = (file_path is not None) 

#==============================================================================
if (__name__ == "__main__"):
    pass
