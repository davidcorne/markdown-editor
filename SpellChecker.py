#!/usr/bin/env python
# Written by: DGC

# python imports
import logging

import enchant

# local imports
import Configuration

#==============================================================================
class Dict(object):
    
    def __init__(self, language, dictionary_dir):
        broker = enchant.Broker()
        broker.set_param("enchant.myspell.dictionary.path", dictionary_dir)
        logging.info(
            "Enchant broker param \"enchant.myspell.dictionary.path\" = %s", 
            broker.get_param("enchant.myspell.dictionary.path")
            )
        word_list_path = Configuration.user_defined_word_list_path()
        self.dict = enchant.DictWithPWL(
            language,
            pwl=word_list_path,
            broker=broker
            )

#==============================================================================
if (__name__ == "__main__"):
    pass
