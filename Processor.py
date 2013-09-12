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

# local imports

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
def add_css(body_html, css):
    """
    Takes raw html and adds CSS to the top, puts it in <html> tags and puts
    it in a body.
    """
    html = [
        OPEN_HEAD,
        css,
        CLOSE_HEAD,
        body_html,
        CLOSE_BODY
        ]
    return "".join(html)

#==============================================================================
def codehilite_extension(line_numbers, css_code_class):
    """
    Returns the extension with correct config for the custom codehilite.
    """
    codehilite = [
        "codehilite(css_class=",
        css_code_class,
        ", linenums=",
        str(line_numbers),
        ")"
        ]
    return "".join(codehilite)

#==============================================================================
class MarkdownRenderer(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def make_html(self, markdown_string):
        raise

    def render(self, markdown_string, css):
        return add_css(self.make_html(markdown_string), css)

#==============================================================================
class MarkdownExtra(MarkdownRenderer):

    def __init__(self, line_numbers, css_code_class):
        super(MarkdownExtra, self).__init__()
        self.renderer = markdown.Markdown(["extra"])

    def make_html(self, markdown_string):
        return self.renderer.convert(markdown_string)

#==============================================================================
class Markdown(MarkdownRenderer):

    def __init__(self, line_numbers, css_code_class):
        super(Markdown, self).__init__()
        self.renderer = markdown.Markdown()

    def make_html(self, markdown_string):
        return self.renderer.convert(markdown_string)

#==============================================================================
class CodeHilite(MarkdownRenderer):

    def __init__(self, line_numbers, css_code_class):
        super(CodeHilite, self).__init__()
        self.renderer = markdown.Markdown(
            extensions=[codehilite_extension(line_numbers, css_code_class)]
            )

    def make_html(self, markdown_string):
        return self.renderer.convert(markdown_string)

#==============================================================================
class MarkdownAll(MarkdownRenderer):

    def __init__(self, line_numbers, css_code_class):
        super(MarkdownAll, self).__init__()
        
        self.renderer = markdown.Markdown(
            extensions=[
                "extra",
                codehilite_extension(line_numbers, css_code_class)
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
                linenos=self.line_numbers,
                cssclass=self.css_code_class,
                )
            highlighted = pygments.highlight(text, lexer, formatter)
            return highlighted

    def __init__(self, line_numbers, css_code_class):
        super(GithubFlavouredMarkdown, self).__init__()
        my_renderer = GithubFlavouredMarkdown.Renderer()
        my_renderer.line_numbers = line_numbers
        my_renderer.css_code_class = css_code_class
        self.renderer = misaka.Markdown(
            my_renderer,
            extensions=misaka.EXT_FENCED_CODE | misaka.EXT_NO_INTRA_EMPHASIS
            )

    def make_html(self, markdown_string):
        return self.renderer.render(markdown_string)

#==============================================================================
if (__name__ == "__main__"):
    pass
