#!/usr/bin/env python
# Written by: DGC

# python imports

# local imports

# done before any other imports in case of errors in them

import Error
Error.set_exception_handler()

# next start logging.
import Log
Log.start_logging()

# now set up localisation
import Localisation
localisation = Localisation.Localiser()

import UserText
UserText.USER_TEXT = UserText.UserText(localisation.language())

#import ToolTips
#UserText.USER_TEXT = UserText.UserText(localisation.language())



import HiddenImports

#==============================================================================
if (__name__ == "__main__"):
    pass
