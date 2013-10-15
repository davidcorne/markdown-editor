#!/usr/bin/env python
# Written by: DGC

# python imports
import enchant

# local imports

#==============================================================================
class Dict(object):
    
    def __init__(self, language, dictionary_dir):
        broker = enchant.Broker()
        broker.set_param("enchant.myspell.dictionary.path", dictionary_dir)
        self.dict = enchant.Dict(language, broker)

#==============================================================================
if (__name__ == "__main__"):
    pass
