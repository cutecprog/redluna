#-------------------------------------------------------------------------------
# This file currently holds the entire game
#-------------------------------------------------------------------------------

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

        # the game
        print question("Ain't 'em pretty?", ["yes","no","mayhaps"])
        print question("What's your favoriate color?", ["scarlet", "violet",   \
                                                "yellow", "torquoise", "aqua", \
                                                "orange", "blue"])
        # exit main()

def question(question, valid_responses, debug=False):
        """ Ask a question and wait for a valid response.

        >>> question("Ain't 'em pretty?", ["yes","no","maybe"], True)
        Ain't 'em pretty?
        - yes
        - no
        - maybe
        'yes'

        """
        print question
        # print valid responses
        for valid_response in valid_responses:
                print "-", valid_response
        while True: # endless loop
                # get user input if not in debug mode
                # else use first item from valid_response list.
                response = raw_input() if not debug else valid_responses[0]
                if response in valid_responses:
                        return response # exit question()

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
