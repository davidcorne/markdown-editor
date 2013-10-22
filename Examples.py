#!/usr/bin/env python
# Written by: DGC

# python imports

# local imports

GITHUB_FLAVOUR_PREVIEW = """
# Github Flavoured Markdown #

This is defined 
[here](https://help.github.com/articles/github-flavored-markdown). Here are 
some of the major differences between this and traditional markdown.

## Fenced Code Blocks ##

In addition to the standard markdown way of specifying code block you can also
surround them with backticks.

<div><pre><span>def</span> <span>hello_world</span><span>():</span>
    <span>print</span><spa>(</span><span>&quot;Hello, World&quot;</span><span>)</span>
</pre></div>

Can be written

<div ><pre><span>```</span>
<span>def</span> <span>hello_world</span><span>()</span><span>:</span>
    <span>print</span><span>(</span><span>&quot;Hello, World&quot;</span><span>)</span>
<span>```</span>
</pre></div>

## Syntax Highlighting##

This is a function written in python.

```python
def hello_world():
    print("Hello, World")
```

You specify the language the code is written in on the backtick line like so.

<div ><pre><span>```python</span>
<span>def</span> <span>hello_world</span><span>()</span><span>:</span>
    <span>print</span><span>(</span><span>&quot;Hello, World&quot;</span><span>)</span>
<span>```</span>
</pre></div>

Note you cannot get syntax highlighting with the standard four space approach.

## Multiple Underscores ##

In standard markdown this_word_sequence would become this<em>word</em>sequence.
This is fixed in GitHub flavoured markdown.

## Newlines ##

In standard markdown you need two newlines to seperate paragraphs, in GitHub
flavoured markdown you only need one.
"""

STANDARD_MARKDOWN = """
# Standard Markdown #

The full syntax for markdown can be found 
[here](http://daringfireball.net/projects/markdown/syntax). 
Here is a small sample.

# Heading 1 #
## Heading 2 ##
### Heading 3 ###

Defined by.

    # Heading 1 #
    ## Heading 2 ##
    ### Heading 3 ###

## Code ##

Code blocks are made by indenting by 4 spaces. Here is an example.

    def hello_world():
        print("Hello, World!")

## Links ##

[shameless link](www.davidcorne.com) made by.

    [shameless link](www.davidcorne.com)

Images are inserted using. 

    ![image](image_location)

## Lists ##

- A list
- Of things

Is just.

    - A list
    - Of things

And an ordered list.

1. One
2. Two
3. ...

Is

    1. One
    2. Two
    3. ...

Or even

    1. One
    1. Two
    1. ...
"""

MARKDOWN_EXTRA = """
# Markdown Extra #

A selection of the features of markdown extra, defined more fully 
[here](http://michelf.ca/projects/php-markdown/extra/).

## Code Blocks ##

This code

```
def hello_world():
    print("Hello, World!")
```

can be defined like this:

    ```
    def hello_world():
        print("Hello, World!")
    ```

or this:

    ~~~
    def hello_world():
        print("Hello, World!")
    ~~~


## Tables ##

You can render tables like so.

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

With the wrong CSS these will not look great however.

Here is the markdown for this.

    First Header  | Second Header
    ------------- | -------------
    Content Cell  | Content Cell
    Content Cell  | Content Cell

## Definition Lists ##

Apple
:   Pomaceous fruit of plants of the genus Malus in 
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.

Is written:

    Apple
    :   Pomaceous fruit of plants of the genus Malus in 
        the family Rosaceae.
    
    Orange
    :   The fruit of an evergreen tree of the genus Citrus.

## Smart Underscores ##

double__underscore__words are not rendered like

double __underscore__ words
"""

MARKDOWN_ALL = """
# Markdown All #

This is a mixture of markdown extra and codehilite. It has the advantages of 
using named language code blocks, definitions, tables and many more features.

## Code ##

This is the main purpose of Markdown All, expressing code easily.

```python
def hello_world():
    print("Hello, World!")
```

The previous code can be expressed in any the following ways.

### Using backticks ###

~~~bash
```python
def hello_world():
    print("Hello, World!")
```
~~~

### Using tildas ###

    ~~~python
    def hello_world():
        print("Hello, World!")
    ~~~

### Using colons ###
Note the 4 spaces.
````
    :::python
    def hello_world():
        print("Hello, World!")
````

### Using a [shebang](http://en.wikipedia.org/wiki/Shebang_(Unix)) with a path ###

Note the 4 spaces.

```bash
    #!/usr/bin/python
    def hello_world():
        print("Hello, World!")
```

### Using a [shebang](http://en.wikipedia.org/wiki/Shebang_(Unix)) without a path ###

Note the 4 spaces.

```bash
    #!python
    def hello_world():
        print("Hello, World!")
```

This gives a large degree of flexibility in how you can specify code. As you 
can see in all of them you can specify the language and as long as it is 
recognised the syntax will be highlighted.
"""

CODEHILITE = """
# Codehilte #

This adds syntax highlighting for named code blocks. The full features of this
extension can be found
[here](http://pythonhosted.org/Markdown/extensions/code_hilite.html).

## Code ###

There are three ways of defining what language the code is written in.

The following code is written in [python](http://www.python.org/).

    :::python
    def hello_world():
        print("Hello, World!")

It can be highlighted using any of these ways. These all augment the standard 
markdown syntax, so each line should be prepended by four spaces.

### Using colons ###

    :::bash
        :::python
        def hello_world():
            print("Hello, World!")

### Using a [shebang](http://en.wikipedia.org/wiki/Shebang_(Unix)) with a path ###

    :::bash
        #!/usr/bin/python
        def hello_world():
            print("Hello, World!")


### Using a [shebang](http://en.wikipedia.org/wiki/Shebang_(Unix)) without a path ###


    :::bash
        #!python
        def hello_world():
            print("Hello, World!")
"""

PREVIEW_MARKDOWN = {
    "markdown": STANDARD_MARKDOWN,
    "markdown_extra": MARKDOWN_EXTRA,
    "github_flavoured_markdown": GITHUB_FLAVOUR_PREVIEW,
    "markdown_all": MARKDOWN_ALL,
    "codehilite": CODEHILITE,
    }

#==============================================================================
def get_preview_markdown(processor):
    if (processor not in PREVIEW_MARKDOWN):
        processor = "markdown"
    return PREVIEW_MARKDOWN[processor]

#==============================================================================
if (__name__ == "__main__"):
    pass
