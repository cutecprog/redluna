#-------------------------------------------------------------------------------
# Test cases for lib.py
#-------------------------------------------------------------------------------

import unittest
from lib import prompt

class TestSequenceFunctions(unittest.TestCase):
        def setUp(self):
                pass

        def test_prompt(self):
                text = "While [torging] through the [toads] the man [trills]."
                test_prompt = None
                try:
                        test_prompt = prompt(text)
                except:
                        print "Error"
                self.assertNotEqual(test_prompt, None)
                self.assertEqual(test_prompt.text, text)
                self.assertEqual(test_prompt.links, ['torging','toads','trills'])

if __name__ == "__main__":
        unittest.main()
