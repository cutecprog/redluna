#-------------------------------------------------------------------------------
# This file currently holds the entire game
#-------------------------------------------------------------------------------

from lib import prompt
import threading
from time import time
from atexit import register  # For clean up function
from os import system, popen

def main():
        story = prompt(20, 60,\
"""Long ago when the [moon shone true] a [girl] like you climbed that tree. Her hair
wasn't as fair and she wasn't nearly as inquisitive of her elder folk. [She died].""")
        init()
        #print story.links
        story.display()
        story.pause()
        t = threading.Thread(target=story.onKeyPress)
        t.daemon = True
        t.start()
        while True:
                if time()-story.head_start_time > .1:
                        story.head_pass()
                if time() - story.prompt_time > 5.0 and                        \
                                        time()-story.tail_start_time > .09:
                        story.tail_pass()
                if not t.isAlive():
                        t = threading.Thread(target=story.onKeyPress)
                        t.daemon = True
                        t.start()

def init():
        print '\033[0m'
        system('setterm -cursor off')
        system('clear')

def loop(story):
        while True:
                if time()-story.head_start_time > .1:
                        story.head_pass()
                if time() - story.prompt_time > 5.0 and                        \
                                        time()-story.tail_start_time > .09:
                        story.tail_pass()

# Exit code
@register
def goodbye():
        system('setterm -cursor on')
        #loop_process.terminate()
        print '\033[0m'
        system('clear')

if __name__ == "__main__":
        from sys import argv
        if "-h" in argv or "--help" in argv:
                # open README and print its contents
                with open("README", "r") as readme_file:
                        print readme_file.read()
                exit()
        main()
