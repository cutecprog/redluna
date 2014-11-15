#-------------------------------------------------------------------------------
# This file currently holds the entire game
#-------------------------------------------------------------------------------

from lib import prompt

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
