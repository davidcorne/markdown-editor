#!/usr/bin/env python
# Written by: DGC

# python imports
import unittest

# local imports
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

    def test_markdown_extra(self, Renderer=MarkdownExtra):
        self.basic_markdown_test(Renderer)
        self.table_test(Renderer)

    def test_codehilite(self, Renderer=CodeHilite):
        self.basic_markdown_test(Renderer)
        self.headers_test(Renderer)
        self.syntax_colons_test(Renderer)
        self.shebang_with_path_test(Renderer)
        self.shebang_without_path_test(Renderer)

    def test_github_flavour(self, Renderer=GithubFlavouredMarkdown):
        # cannot use basic_markdown_test() as github uses weird newlines
        self.backticks_test(Renderer)
        self.backticks_highlight_test(Renderer)

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
        
    def basic_markdown_test(self, Renderer):
        self.headers_test(Renderer)
        self.ordered_list_test(Renderer)
        self.unordered_list_test(Renderer)
        self.link_test(Renderer)
        self.image_test(Renderer)
        self.code_test(Renderer)

    def headers_test(self, Renderer):
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
        result = unicode("""<h1>Header 1</h1>
<h2>Header 2</h2>
<h3>Header 3</h3>
<h4>Header 4</h4>
<h5>Header 5</h5>
<h6>Header 6</h6>""")
        self.assertEqual(html, result)

    def ordered_list_test(self, Renderer):
        markdown = """
1. thing
1. another thing.
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        result = unicode("""<ol>
<li>thing</li>
<li>another thing.</li>
</ol>""")
        self.assertEqual(html, result)
        pass

    def unordered_list_test(self, Renderer):
        markdown = """
- thing
- another thing.
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        result = unicode("""<ul>
<li>thing</li>
<li>another thing.</li>
</ul>""")
        self.assertEqual(html, result)
        pass

    def link_test(self, Renderer):
        markdown = """
[shameless link](www.davidcorne.com)
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        result = unicode("""<p><a href="www.davidcorne.com">shameless link</a></p>""")
        self.assertEqual(html, result)
        pass

    def image_test(self, Renderer):
        markdown = """
![image](image_location)
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        result = unicode("""<p><img alt="image" src="image_location" /></p>""")
        self.assertEqual(html, result)
        pass

    def code_test(self, Renderer):
        markdown = """
Paragraph

    code
        
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        num = html.count("pre")
        self.assertEqual(num, 2)
    
    def syntax_colons_test(self, Renderer):
        markdown = """
    ::python
    def hello_world():
        print("Hello, World!")
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        result = unicode("""<div><pre><span class="k">def</span> <span class="nf">hello_world</span><span class="p">():</span>
    <span class="k">print</span><span class="p">(</span><span class="s">&quot;Hello, World!&quot;</span><span class="p">)</span>
</pre></div>""")
        self.assertEqual(result, html)

    def shebang_with_path_test(self, Renderer):
        markdown = """
    #!/usr/bin/python
    def hello_world():
        print("Hello, World!")
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        num = html.count("pre")
        self.assertEqual(num, 2)

    def shebang_without_path_test(self, Renderer):
        markdown = """
    #!python
    def hello_world():
        print("Hello, World!")
"""
        renderer = Renderer(False, "")
        html = renderer.make_html(markdown)
        num = html.count("pre")
        self.assertEqual(num, 2)

    def backticks_test(self, Renderer):
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

    def backticks_highlight_test(self, Renderer):
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

    def table_test(self, Renderer):
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