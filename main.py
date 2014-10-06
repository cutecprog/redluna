#------------------------------------------------------------------------------
# This file currently holds the entire game.
#------------------------------------------------------------------------------

from sys import argv
def main():
        if "-h" in argv or "--help" in argv:
                print "Red Luna is a text adventure game."
                return # Exit main()
        print "Red Luna"
        print question("Ain't 'em pretty?", ["yes","no","the question is wrong"])

def question(question, valid_responses, debug=False):
        """ Ask a question and wait for a valid response.
        
        >>> question("Ain't 'em pretty?", ["yes","no","the question is wrong"], True)
        Ain't 'em pretty?
        - yes
        - no
        - the question is wrong
        'yes'
        """
        print question
        for valid_response in valid_responses:
                print "-", valid_response
        while True:
                response = raw_input() if not debug else valid_responses[0]
                if response in valid_responses:
                        return response

# Check if this file is being executed
if __name__=="__main__":
        from doctest import testmod
        testmod()
        main() # run my function
