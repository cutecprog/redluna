#-------------------------------------------------------------------------------
# This file currently holds the entire game
#-------------------------------------------------------------------------------

from lib import prompt
import threading
from time import time, sleep
from atexit import register  # For clean up function
from os import system, popen
from tty import setraw
from termios import tcsetattr, tcgetattr, TCSADRAIN
from sys import stdin

# Globals
fd = stdin.fileno()
old_settings = tcgetattr(fd)

def main():
        story = None
        with open('data/start', 'r') as f:
                story = prompt(20, 60, f.read())
        init()
        #print story.links
        story.display()
        story.pause()
        t = threading.Thread(target=loop, args=[story])
        t.daemon = True
        t.start()
        while True:
                story.onKeyPress()

def init():
        print '\033[0m'
        system('setterm -cursor off')
        setraw(fd)
        system('clear')

def loop(story):
        while True:
                story.debug()
                if time()-story.head_start_time > .1:
                        story.head_pass()
                if time() - story.prompt_time > 5.0 and                        \
                                        time()-story.tail_start_time > .09:
                        story.tail_pass()

# Exit code
@register
def goodbye():
        system('setterm -cursor on')
        print '\033[0m'
        tcsetattr(fd, TCSADRAIN, old_settings)
        system('clear')

if __name__ == "__main__":
        from sys import argv
        if "-h" in argv or "--help" in argv:
                # open README and print its contents
                with open("README", "r") as readme_file:
                        print readme_file.read()
                exit()
        main()
