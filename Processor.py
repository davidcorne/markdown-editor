#!/usr/bin/env python
# Written by: DGC

# python imports

import abc
import markdown

# local imports

#import misaka_test

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
class GithubFlavouredMarkdown(MarkdownRenderer):

    def render(self, markdown_string):
        return "Github"

#==============================================================================
if (__name__ == "__main__"):
    pass
