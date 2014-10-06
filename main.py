#------------------------------------------------------------------------------
# This file currently holds the entire game.
#------------------------------------------------------------------------------

# Example function demonstrating project coding style
def foo(bar):
        """ Print parameter bar and return a meaningless string.

        >>> foo("Foo doesn't really do anything")
        Foo doesn't really do anything
        'what foo returns'

        """
        print bar
        return "what foo returns"

def main(debug=False):
        """ Run the game.

        >>> main(True)
        Red Luna

        """
        print "Red Luna"
        if debug:
                return # Exit main

        # the game
        print question("Ain't 'em pretty?", ["yes","no","the question is wrong"])

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
        while True:
                # get user input if not in debug mode
                # else use first item from valid_response list.
                response = raw_input() if not debug else valid_responses[0]
                if response in valid_responses:
                        return response

# if this file is being executed 
# then check for commend line args, run doctests, run main()
if __name__=="__main__":
        from sys import argv
        if "-h" in argv or "--help" in argv:
                print "Red Luna is a text adventure game.\n"
                print "Options:"
                print " -h or --help\t\tPrints this menu"
                print " -v\t\t\tVerbose mode for doctest\n"
                exit()

        from doctest import testmod
        testmod() # run all doctest
        main() # run my function
