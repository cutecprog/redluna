#-------------------------------------------------------------------------------
# Test cases for lib.py
#-------------------------------------------------------------------------------

import unittest
from lib import word

class TestSequenceFunctions(unittest.TestCase):
        def setUp(self):
                self.meaningless = word()

        def test_word(self):
                self.assertEqual(type(self.meaningless.get_synonyms()), list)
                friend = ['friend','pal','conrad','ally']
                self.assertEqual(word(friend).get_synonyms(), friend)


if __name__ == "__main__":
        unittest.main()
