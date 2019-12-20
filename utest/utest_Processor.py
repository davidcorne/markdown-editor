#!/usr/bin/env python
# Written by: DGC

# python imports
import sys
import unittest

# local imports
sys.path.append("..")
from Processor import *

#==============================================================================
class utest_Processor(unittest.TestCase):
    RENDERERS = [
        Markdown,
        MarkdownExtra,
        CodeHilite,
        GithubFlavouredMarkdown,
        MarkdownAll,
        ]
    
    def test_markdown(self, Renderer=Markdown):
        self.basic_markdown_test(Renderer)
        self.code_test(Renderer)

    def test_markdown_extra(self, Renderer=MarkdownExtra):
        self.basic_markdown_test(Renderer)
        self.code_test(Renderer)
        self.table_test(Renderer)

    def test_codehilite(self, Renderer=CodeHilite):
        self.basic_markdown_test(Renderer)
        self.code_test(Renderer)
        #self.syntax_colons_test(Renderer)
        #self.shebang_with_path_test(Renderer)
        #self.shebang_without_path_test(Renderer)

    def test_github_flavour(self, Renderer=GithubFlavouredMarkdown):
        self.basic_markdown_test(Renderer)
        self.backticks_test(Renderer)
        #self.backticks_highlight_test(Renderer)

    def test_markdown_all(self):
        self.test_markdown(MarkdownAll)
        self.test_markdown_extra(MarkdownAll)
        self.test_codehilite(MarkdownAll)
        self.test_github_flavour(MarkdownAll)

    def test_css(self):
        css = "THIS IS CSS"
        markdown = "Hey"
        for Renderer in self.RENDERERS:
            renderer = Renderer(False, "")
            html = renderer.render(markdown, css)
            self.assertIn(css, html)
            self.assertIn(markdown, html)

    def basic_markdown_test(self, Renderer=Markdown):
        self.headers_test(Renderer)
        self.ordered_list_test(Renderer)
        self.unordered_list_test(Renderer)
        self.link_test(Renderer)
        self.image_test(Renderer)

    def headers_test(self, Renderer=Markdown):
        markdown = """
# Header 1 #
## Header 2 ##
### Header 3 ###
#### Header 4 ####
##### Header 5 #####
###### Header 6 ######
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        self.assertEqual(html.count("h1"), 2)
        self.assertEqual(html.count("h2"), 2)
        self.assertEqual(html.count("h3"), 2)
        self.assertEqual(html.count("h4"), 2)
        self.assertEqual(html.count("h5"), 2)
        self.assertEqual(html.count("h6"), 2)

    def ordered_list_test(self, Renderer=Markdown):
        markdown = """
1. thing
1. another thing.
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        self.assertEqual(html.count("<li>"), 2)
        self.assertEqual(html.count("</li>"), 2)
        self.assertEqual(html.count("ol"), 2)

    def unordered_list_test(self, Renderer=Markdown):
        markdown = """
- thing
- another thing.
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        self.assertEqual(html.count("<li>"), 2)
        self.assertEqual(html.count("</li>"), 2)
        self.assertEqual(html.count("ul"), 2)

    def link_test(self, Renderer=Markdown):
        markdown = """
[shameless link](www.davidcorne.com)
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        self.assertIn(
            "<p><a href=\"www.davidcorne.com\">shameless link</a></p>", 
            html
            )

    def image_test(self, Renderer=Markdown):
        markdown = """
![image](image_location)
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        result = unicode("""<p><img alt="image" src="image_location" /></p>""")
        self.assertIn("<p>", html)
        self.assertIn("</p>", html)
        self.assertIn("<img ", html)
        self.assertIn("alt=\"image\"", html)
        self.assertIn("src=\"image_location\"", html)

    def code_test(self, Renderer=Markdown):
        markdown = """
Paragraph

    code
        
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        num = html.count("pre")
        self.assertEqual(num, 2)
    
    def syntax_colons_test(self, Renderer=CodeHilite):
        markdown = """
    ::python
    def hello_world():
        print("Hello, World!")
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        result = unicode("""<div><pre><span class="k">def</span> <span class="nf">hello_world</span><span class="p">():</span>
    <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Hello, World!&quot;</span><span class="p">)</span>
</pre></div>""")
        self.assertEqual(result, html)
        # 2 keywords
        self.assertEqual(html.count("<span class=\"k\">"), 2)
        # 1 name of function
        self.assertEqual(html.count("<span class=\"nf\">"), 1)
        # 3 parenteses [(), ( and )]
        self.assertEqual(html.count("<span class=\"p\">"), 3)
        # 1 string
        self.assertEqual(html.count("<span class=\"s\">"), 1)

    def shebang_with_path_test(self, Renderer=CodeHilite):
        markdown = """
    #!/usr/bin/python
    def hello_world():
        print("Hello, World!")
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        num = html.count("pre")
        self.assertEqual(num, 2)
        # 2 keywords
        self.assertEqual(html.count("<span class=\"k\">"), 2)
        # 1 name of function
        self.assertEqual(html.count("<span class=\"nf\">"), 1)
        # 3 parenteses [(), ( and )]
        self.assertEqual(html.count("<span class=\"p\">"), 3)
        # 1 string
        self.assertEqual(html.count("<span class=\"s\">"), 1)

    def shebang_without_path_test(self, Renderer=CodeHilite):
        markdown = """
    #!python
    def hello_world():
        print("Hello, World!")
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        num = html.count("pre")
        self.assertEqual(num, 2)
        # 2 keywords
        self.assertEqual(html.count("<span class=\"k\">"), 2)
        # 1 name of function
        self.assertEqual(html.count("<span class=\"nf\">"), 1)
        # 3 parenteses [(), ( and )]
        self.assertEqual(html.count("<span class=\"p\">"), 3)
        # 1 string
        self.assertEqual(html.count("<span class=\"s\">"), 1)

    def backticks_test(self, Renderer=GithubFlavouredMarkdown):
        code = """
```python
def hi():
    print("Hi")
```
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(code)
        num = html.count("pre")
        self.assertEqual(num, 2)

    def backticks_highlight_test(self, Renderer=GithubFlavouredMarkdown):
        code = """
```python
def hi():
    print("Hi")
```
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(code)
        # 2 keywords
        self.assertEqual(html.count("<span class=\"k\">"), 2)
        # 1 name of function
        self.assertEqual(html.count("<span class=\"nf\">"), 1)
        # 3 parenteses [(), ( and )]
        self.assertEqual(html.count("<span class=\"p\">"), 3)
        # 1 string
        self.assertEqual(html.count("<span class=\"s\">"), 1)

    def table_test(self, Renderer=MarkdownExtra):
        table = """
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(table)
        result = unicode("""<table>
<thead>
<tr>
<th>First Header</th>
<th>Second Header</th>
</tr>
</thead>
<tbody>
<tr>
<td>Content Cell</td>
<td>Content Cell</td>
</tr>
<tr>
<td>Content Cell</td>
<td>Content Cell</td>
</tr>
</tbody>
</table>""")
        self.assertEqual(html, result)

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
