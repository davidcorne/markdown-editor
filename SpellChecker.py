#!/usr/bin/env python
# Written by: DGC

# python imports
import logging

import enchant

# local imports

#==============================================================================
class Dict(object):
    
    def __init__(self, language, dictionary_dir, word_list_path):
        broker = enchant.Broker()
        broker.set_param("enchant.myspell.dictionary.path", dictionary_dir)
        logging.info(
            "Enchant broker param \"enchant.myspell.dictionary.path\" = %s", 
            broker.get_param("enchant.myspell.dictionary.path")
            )
        logging.info("Personal word list file: \"%s\"", word_list_path)
        self.dict = enchant.DictWithPWL(
            language,
            pwl=word_list_path,
            broker=broker
            )

#==============================================================================
if (__name__ == "__main__"):
    pass
