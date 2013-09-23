#!/usr/bin/env python
# Written by: DGC

# python imports
import unittest

# local imports
import html

#==============================================================================
class utest_html(unittest.TestCase):
    
    def test_simple(self):
        p = html.Node("p")
        self.assertEqual(p.to_string(), "<p />")
        p = html.Node("p", "hello")
        self.assertEqual(p.to_string(), "<p >hello</p>")

    def test_attributes(self):
        img = html.Node("img")
        img["src"] = "path"
        self.assertEqual(img.to_string(), "<img src=\"path\" />")

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
