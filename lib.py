#-------------------------------------------------------------------------------
# Support library for the game
#-------------------------------------------------------------------------------

class word(object):
        def __init__(self, synonym_list = []):
                self.synonym_list = synonym_list

        def get_synonyms(self):
                return ()

        def get_conotation(self):
                """ Return the feeling of the word as data.

                """
                return (0, 3, 2, 5)

class hyper_word(word):
        def __init__(self, synonym_list = []):
                Base.__init__(self, synonym_list)
