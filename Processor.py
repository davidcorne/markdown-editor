#!/usr/bin/env python
# Written by: DGC

# python imports

import abc
import cgi
import markdown
import misaka
import pygments
import pygments.lexers
import pygments.formatters
import os

# local imports

import Configuration

OPEN_HEAD = """<html>
<head>
  <title></title>
  <meta http-equiv="content-type" content="text/html; charset=None">
  <style type="text/css">
"""

CLOSE_HEAD = """</style>
</head>
<body>"""

CLOSE_BODY = "</body></html>"

#==============================================================================
class MarkdownRenderer(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def make_html(self, markdown_string):
        raise

    def render(self, markdown_string):
        return self.add_css(self.make_html(markdown_string))

    def add_css(self, raw_html):
        """
        Takes raw html and adds CSS to the top, puts it in <html> tags and puts
        it in a body.
        """
        html = [
            OPEN_HEAD,
            Configuration.MARKDOWN_CSS,
            Configuration.CODE_CSS,
            CLOSE_HEAD,
            raw_html,
            CLOSE_BODY
            ]
        return "".join(html)

#==============================================================================
class MarkdownExtra(MarkdownRenderer):

    def __init__(self):
        super(MarkdownExtra, self).__init__()
        self.renderer = markdown.Markdown(["extra"])

    def make_html(self, markdown_string):
        return self.renderer.convert(markdown_string)

#==============================================================================
class Markdown(MarkdownRenderer):

    def __init__(self):
        super(Markdown, self).__init__()
        self.renderer = markdown.Markdown()

    def make_html(self, markdown_string):
        return self.renderer.convert(markdown_string)

#==============================================================================
class CodeHilite(MarkdownRenderer):

    def __init__(self):
        super(CodeHilite, self).__init__()
        self.renderer = markdown.Markdown(extensions=[codehilite_extension()])

    def make_html(self, markdown_string):
        return self.renderer.convert(markdown_string)

#==============================================================================
class MarkdownAll(MarkdownRenderer):

    def __init__(self):
        super(MarkdownAll, self).__init__()
        
        self.renderer = markdown.Markdown(
            extensions=[
                "extra",
                codehilite_extension()
                ]
            )

    def make_html(self, markdown_string):
        return self.renderer.convert(markdown_string)

#==============================================================================
class GithubFlavouredMarkdown(MarkdownRenderer):

    #==========================================================================
    class Renderer(misaka.HtmlRenderer, misaka.SmartyPants):

        def block_code(self, text, language):
            try:
                lexer = pygments.lexers.get_lexer_by_name(
                    language,
                    stripall=True
                    )
            except pygments.util.ClassNotFound:
                return cgi.escape(text, quote=True)
            formatter = pygments.formatters.HtmlFormatter(
                linenos=Configuration.OPTIONS["display_line_numbers"]
                )
            highlighted = pygments.highlight(text, lexer, formatter)
            return highlighted

    def __init__(self):
        super(GithubFlavouredMarkdown, self).__init__()
        my_renderer = GithubFlavouredMarkdown.Renderer()
        self.renderer = misaka.Markdown(
            my_renderer,
            extensions=misaka.EXT_FENCED_CODE | misaka.EXT_NO_INTRA_EMPHASIS
            )

    def make_html(self, markdown_string):
        return self.renderer.render(markdown_string)

#==============================================================================
def codehilite_extension():
    """
    Returns the extension with correct config for the custom codehilite.
    """
    line_numbers = Configuration.OPTIONS["display_line_numbers"]
    codehilite = [
        "codehilite(css_class=highlight, linenums=",
        str(line_numbers),
        ")"
        ]
    return "".join(codehilite)

#==============================================================================
if (__name__ == "__main__"):
    pass
