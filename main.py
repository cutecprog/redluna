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
from sys import stdin, stderr

# Globals
fd = None
old_settings = None
error_message = ""
size = popen('stty size','r').read()

def main():
        global error_message
        story = None
        rows, cols = size.split()
        rows = int(rows)
        cols = int(cols)
        if rows < 16 or cols < 80:
                error_message += "\033[91m\033[1mError:\033[0m screen is smaller than 16x80\n"
                return
        y = (rows - 7)/2
        if y < 8:
                y = 8
        x = (cols - 80)/2 + 1
        with open('data/start', 'r') as f:
                story = prompt(y, x, f.read())
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
        global fd
        global old_settings
        print '\033[0m'
        system('setterm -cursor off')
        fd = stdin.fileno()
        old_settings = tcgetattr(fd)
        setraw(fd)
        system('clear')

def loop(story):
        global error_message
        last_window_check = time()
        while True:
                #story.debug()
                if time()-story.head_start_time > .1:
                        story.head_pass()
                if time() - story.prompt_time > 5.0 and                        \
                                        time()-story.tail_start_time > .09:
                        story.tail_pass()
                if time() - last_window_check > 2:
                        if size == popen('stty size','r').read():
                                last_window_check = time()
                        else:
                                error_message += "\033[91m\033[1mError:\033[0m screen size changed\n"
                                exit()

# Exit code
@register
def goodbye():
        if fd or old_settings:
                system('setterm -cursor on')
                print '\033[0m'
                tcsetattr(fd, TCSADRAIN, old_settings)
                system('clear')
        if error_message != "":
                print error_message

if __name__ == "__main__":
        from sys import argv
        if "-h" in argv or "--help" in argv:
                # open README and print its contents
                with open("README", "r") as readme_file:
                        print readme_file.read()
                exit()
        main()
