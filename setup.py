from distutils.core import setup
try:
    import py2exe
except ImportError:
    pass

with open("wiki/Home.md", "r") as wiki_home:
    description = wiki_home.read()

# not strictly a good idea as it uses revision number to identify a changeset
with open(".hg/cache/branchheads", "r") as mercurial_file:
    first_line = mercurial_file.readline()
    mercurial_revision = first_line.split()[1]

setup(
    name="MarkdownEditor",
    version="0." + mercurial_revision,
    author="David Corne",
    author_email="davidcorne@gmail.com",
    url="https://bitbucket.org/davidcorne/markdown-editor",
    description="A fully featured cross platform markdown editor.",
    long_description=description,
    windows=["MarkdownEditor.py"],
    options={
        "py2exe":{
            "ascii":False,
            "optimize":2,
            "includes" : ["sip", "PyQt4"],
            "dist_dir": "py2exe",
            #"bundle_files": 1 # bundle everything into the exe
            }
        }
    )
