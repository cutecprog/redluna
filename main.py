#------------------------------------------------------------------------------
# This file currently holds the entire game.
#------------------------------------------------------------------------------

def main():
        print "Red Luna"
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
                response = raw_input() if not debug else valid_responses[0]
                if response in valid_responses:
                        return response

# check if this file is being executed
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
