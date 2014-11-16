#-------------------------------------------------------------------------------
# This file currently holds the entire game
#-------------------------------------------------------------------------------

from lib import prompt
import multiprocessing
from time import time
from atexit import register  # For clean up function
from os import system

story = prompt(20, 60,\
"""Long ago when the [moon shone true] a [girl] like you climbed that tree. Her hair
wasn't as fair and she wasn't nearly as inquisitive of her elder folk. [She died].""")

def main():
        global story
        init()
        story.display()
        story.prompt_time = time()
        loop_process.start()
        while True:
                story.onKeyPress()

def init():
        print '\033[0m'
        system('setterm -cursor off')
        system('clear')

def loop():
        global story
        while True:
                if time()-story.head_start_time > .1:
                        story.head_pass()
                if time() - story.prompt_time > 5.0 and                        \
                                        time()-story.tail_start_time > .09:
                        story.tail_pass()
loop_process = multiprocessing.Process(name='loop', target=loop)

# Exit code
@register
def goodbye():
        print '\033[0m'
        system('setterm -cursor on')
        loop_process.terminate()
        system('clear')

if __name__ == "__main__":
        from sys import argv
        if "-h" in argv or "--help" in argv:
                # open README and print its contents
                with open("README", "r") as readme_file:
                        print readme_file.read()
                exit()
        main()
