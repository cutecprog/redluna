#------------------------------------------------------------------------------
# This file currently holds the entire game.
#------------------------------------------------------------------------------

from sys import argv
def main():
        if "-h" in argv or "--help" in argv:
                print "Red Luna is a text adventure game."
                return # Exit main()
        print "Red Luna"

if __name__=="__main__":
        main()
