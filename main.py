#------------------------------------------------------------------------------
# This file currently holds the entire game.
#------------------------------------------------------------------------------

from sys import argv
def main():
        if "-h" in argv or "--help" in argv:
                print "Red Luna is a text adventure game."
                return # Exit main()
        print "Red Luna"

def question(question, responses):
        """ Ask a question and wait for a valid response.
        
        >>> question("Ain't 'em pretty?", ["yes","no","the question is wrong"])
        2
        """
        return 0

# Check if this file is being executed
if __name__=="__main__":
        main() # run my function
