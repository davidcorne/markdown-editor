from distutils.core import setup
import py2exe

setup(
    windows=["MarkdownEditor.py"],
    options={
        "py2exe":{
            "ascii":False,
            "optimize":2,
            "includes" : ["sip", "PyQt4"],
            #"bundle_files": 1 # bundle everything into the exe
            }
        }
    )
