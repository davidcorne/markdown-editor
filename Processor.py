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

CLOSE_BODY = "</body>"

#==============================================================================
class MarkdownRenderer(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def render(self, markdown_string):
        raise

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

    def render(self, markdown_string):
        html = markdown.markdown(markdown_string, ["extra"])
        return self.add_css(html)

#==============================================================================
class Markdown(MarkdownRenderer):

    def __init__(self):
        super(Markdown, self).__init__()

    def render(self, markdown_string):
        html = markdown.markdown(markdown_string)
        return self.add_css(html)

#==============================================================================
class GithubFlavouredMarkdown(MarkdownRenderer):
    
    #==========================================================================
    class Renderer(misaka.HtmlRenderer, misaka.SmartyPants):
    
        def block_code(self, text, language):
            lexer = pygments.lexers.get_lexer_by_name(language, stripall=True)
            formatter = pygments.formatters.HtmlFormatter(linenos=True)#, cssclass="dgc")
            formatter.get_style_defs("")
            highlighted = pygments.highlight(text, lexer, formatter)
            #print highlighted
            return highlighted

    def __init__(self):
        super(GithubFlavouredMarkdown, self).__init__()
        my_renderer = GithubFlavouredMarkdown.Renderer()
        self.renderer = misaka.Markdown(
            my_renderer, 
            extensions=misaka.EXT_FENCED_CODE | misaka.EXT_NO_INTRA_EMPHASIS
            )

    def render(self, markdown_string):
        rendered = self.renderer.render(markdown_string)
        return self.add_css(rendered)

#==============================================================================
if (__name__ == "__main__"):
    pass
