#-------------------------------------------------------------------------------
# This file currently holds the entire game
#-------------------------------------------------------------------------------

from lib import prompt
import threading
from time import time
from atexit import register  # For clean up function
from os import system, popen
from tty import setraw
from termios import tcsetattr, tcgetattr, TCSADRAIN
from sys import stdin, stderr, stdout

# Globals
error_message = ""
size = popen('stty size','r').read()

def main():
        #init()
        system('clear')
        story = prompt(stty_center(), 'start')
        register(story.goodbye)
        story.display()
        story.pause()
        stty_check()
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

def stty_check():
        global error_message
        if size != popen('stty size','r').read():
                error_message += "screen size changed during runtime\n"
                exit()

def stty_center():
        global error_message
        rows, cols = size.split()
        rows = int(rows)
        cols = int(cols)
        if rows < 16 or cols < 80: # stty invalid
                error_message += "screen is smaller than 16x80\n"
                exit()
        y = (rows - 7)/2
        if y < 8:
                y = 8
        x = (cols - 80)/2 + 1
        return y, x

if __name__ == "__main__":
        from sys import argv
        if "-h" in argv or "--help" in argv:
                # open README and print its contents
                with open("README", "r") as readme_file:
                        print readme_file.read()
                exit()
        main()
