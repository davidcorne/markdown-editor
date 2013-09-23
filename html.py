#!/usr/bin/env python
# Written by: DGC

# python imports

# local imports

#==============================================================================
class Node(object):
    """
    A class to encapsulate creation of html nodes.

    Intended to be used like:

    img = html.Node("img")
    img["src"] = "C:\path\image.png"
    img["title"] = "title"
    img.to_string()
    """

    def __init__(self, name, contents=None):
        self.name = name
        self.contents = contents
        self.attributes = dict()

    def __setitem__(self, key, value):
        self.attributes[key] = value

    def to_string(self):
        html = [
        "<",
        self.name,
        " "
        ]
        for key in self.attributes:
            attribute_html = [
                key,
                "=\"",
                self.attributes[key],
                "\" ",
                ]
            html += attribute_html
        if self.contents:
            contents_html = [
                ">",
                self.contents,
                "</",
                self.name,
                ">",
                ]
            html += contents_html
        else:
            html.append("/>")
        return "".join(html)

#==============================================================================
if (__name__ == "__main__"):
    pass
