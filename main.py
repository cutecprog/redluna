#-------------------------------------------------------------------------------
# This file currently holds the entire game
#-------------------------------------------------------------------------------

from lib import prompt
import multiprocessing
from time import time

def main(args, debug=False):
        """ Print args and if not in debug mode start the game.

        >>> main("This could be anything", True)
        This could be anything
        'what is returned when debug is True'

        """
        print args
        # if debug mode, return a meaningless string that the doctest expects
        if debug:
                return "what is returned when debug is True" # exit main()

        story = prompt(20, 60,\
"""Long ago when the [moon shone true] a [girl] like you climbed that tree. Her hair
wasn't as fair and she wasn't nearly as inquisitive of her elder folk. [She died].""")

        story.head_pass()
        while True:
                if time()-story.head_start_time > .1:
                        story.head_pass()
                if time() - story.prompt_time > 5 and                        \
                                        time()-story.head_start_time > .09:
                        story.tail_pass()
        # end game

# if this file is being executed 
# then check for commend line args, run doctests, run main()
if __name__ == "__main__":
        from sys import argv
        if "-h" in argv or "--help" in argv:
                # open README and print its contents
                with open("README", "r") as readme_file:
                        print readme_file.read()
                exit()

        from doctest import testmod
        testmod() # run all doctest
        main("Red Luna") # run my function
