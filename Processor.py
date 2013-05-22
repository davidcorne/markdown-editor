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

#==============================================================================
class MarkdownRenderer(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def render(self, markdown_string):
        raise

#==============================================================================
class MarkdownExtra(MarkdownRenderer):

    def render(self, markdown_string):
        return markdown.markdown(markdown_string, ["extra"])

#==============================================================================
class Markdown(MarkdownRenderer):

    def render(self, markdown_string):
        return markdown.markdown(markdown_string)

#==============================================================================
class GithubFlavouredMarkdownRenderer(misaka.HtmlRenderer, misaka.SmartyPants):
    
    def block_code(self, text, language):
        try:
            lexer = pygments.lexers.get_lexer_by_name(language, stripall=True)
        except pygments.util.ClassNotFound:
            code = [
                "\n<pre><code>",
                cgi.escape(text.strip()),
                "</code></pre>\n",
                ]
            return "".join(code)
        formatter = pygments.formatters.HtmlFormatter(full=True)
        return pygments.highlight(text, lexer, formatter)

#==============================================================================
class GithubFlavouredMarkdown(MarkdownRenderer):
    
    def __init__(self):
        my_renderer = GithubFlavouredMarkdownRenderer()
        self.renderer = misaka.Markdown(
            my_renderer, 
            extensions=misaka.EXT_FENCED_CODE | misaka.EXT_NO_INTRA_EMPHASIS
            )

    def render(self, markdown_string):
        return self.renderer.render(markdown_string)

#==============================================================================
if (__name__ == "__main__"):
    pass
