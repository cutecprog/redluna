#-------------------------------------------------------------------------------
# This file currently holds the entire game
#-------------------------------------------------------------------------------

from lib import prompt
import threading
from time import time
from os import system
from atexit import register

def main():
        #init()
        system('clear')
        story = prompt('start')
        register(story.goodbye)
        story.display()
        story.pause()
        t = threading.Thread(target=loop, args=[story])
        t.daemon = True
        t.start()
        while True:
                story.onKeyPress()

def loop(story):
        last_stty_check = time()
        while story.prompt_time:
                #story.debug()
                if time()-story.head_start_time > .1:
                        story.head_pass()
                if time() - story.prompt_time > 5.0 and                        \
                                        time()-story.tail_start_time > .09:
                        story.tail_pass()
                if time() - last_stty_check > 6:
                        stty_check()
                        last_stty_check = time()

if __name__ == "__main__":
        from sys import argv
        if "-h" in argv or "--help" in argv:
                # open README and print its contents
                with open("README", "r") as readme_file:
                        print readme_file.read()
                exit()
        main()
