#!/usr/bin/env python
# Written by: DGC

# done before any other imports in case of errors in them

import Error
Error.set_exception_handler()

# python imports
import sys

# local imports
import MarkdownEditor
import PyinstallerHiddenImports

#==============================================================================
def main():
    # take over with real error handling 
    app = MarkdownEditor.MarkdownEditorApp(sys.argv)
    editor = MarkdownEditor.MarkdownEditor(sys.argv[1:])
    sys.exit(app.exec_())

#==============================================================================
if (__name__ == "__main__"):
    main()
