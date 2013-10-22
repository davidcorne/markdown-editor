#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import unittest

# local imports
sys.path.append("..")
import Examples

#==============================================================================
class utest_Examples(unittest.TestCase):
    PROCESSORS = [
        "markdown",
        "markdown_extra",
        "markdown_all",
        "codehilite",
        "github_flavoured_markdown",
        ]

    def test_existence(self):
        """
        This tests that for each processor there is an example.
        """
        for processor in self.PROCESSORS:
            self.assertIn(processor, Examples.PREVIEW_MARKDOWN)
        
#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
