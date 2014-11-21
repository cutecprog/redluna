#-------------------------------------------------------------------------------
# Support library for the game
#-------------------------------------------------------------------------------

from time import time
from re import compile, match, sub
from sys import stdin, stdout, stderr
from os import system, popen, read
from termios import tcsetattr, tcgetattr, TCSADRAIN
from tty import setraw

command_list = compile('(^end game stint)\s*$|(^spare)\s*$|(^spare as )(\w+)\s*$')

v_bar = b'\xe2\x94\x82'
h_bar = b'\xe2\x94\x80'
bl_corner = b'\xe2\x95\xb0'
br_corner = b'\xe2\x95\xaf'
tl_corner = b'\xe2\x95\xad'
tr_corner = b'\xe2\x95\xae'
bl_square_corner = b'\xe2\x94\x94'

fd = stdin.fileno()
old_settings = tcgetattr(fd)
error_message = ""
size = popen('stty size','r').read()

def print_loc(text, y, x):
        print("\033[%s;%sH" % (y,x) + text)

def stty_center():
        global error_message
        rows, cols = size.split()
        rows = int(rows)
        cols = int(cols)
        if rows < 16 or cols < 80: # stty invalid
                #error_message += "screen is smaller than 16x80\n"
                line = "screen is smaller than 16x80\n"
                stderr.write("\033[0;91;1mError:\033[0m "+line+'\n')
                exit()
        y = (rows - 7)/2
        if y < 8:
                y = 8
        x = (cols - 80)/2 + 1
        return y, x

def stty_check():
        global error_message
        if size != popen('stty size','r').read():
                error_message += "screen size changed during runtime\n"
                exit()

class prompt(object):
        def __init__(self, link = "", pos = stty_center(), start_head = 0, start_tail = 5):
                self.text = ""
                self._load_text(link)
                self.length = len(self.text)
                self.links = ""
                self._generate_links()
                self.y          = pos[0]
                self.x          = pos[1]
                self.head       = 0
                self.head_x     = 0
                self.head_y     = 0
                self.tail       = 0
                self.tail_x     = 0
                self.tail_y     = 0
                self.text_color = '\033[0m'
                self.user_input = ""
                self.prompt_time = time()
                self.head_start_time = 0
                self.tail_start_time = 0
                self.locked = 0
                print '\033[0m'
                system('setterm -cursor off')
                setraw(fd)

        def goodbye(self):
                if fd or old_settings:
                        system('clear')
                        system('setterm -cursor on')
                        tcsetattr(fd, TCSADRAIN, old_settings)
                if error_message != "":
                        for line in error_message.split('\n')[:-1]:
                                stderr.write("\033[0;91;1mError:\033[0m "+line+'\n')
                        print ""
                stdout.write('\033[0m')

        def debug(self):
                if self.locked:
                        return
                self.locked += 1
                print "\033[0m"
                print_loc("head:",          2, 62)
                print_loc("x:",             3, 65)
                print_loc("y:",             4, 65)
                print_loc("tail:",          5, 62)
                print_loc("x:",             6, 65)
                print_loc("y:",             7, 65)
                print_loc(str(self.head)   + "  ", 2, 86)
                print_loc(str(self.head_x) + "  ", 3, 86)
                print_loc(str(self.head_y) + "  ", 4, 86)
                print_loc(str(self.tail)   + "  ", 5, 86)
                print_loc(str(self.tail_x) + "  ", 6, 86)
                print_loc(str(self.tail_y) + "  ", 7, 86)
                self.locked -= 1

        def head_pass(self):
                if self.locked:
                        return
                self.head_start_time = time()
                if self.head >= self.length:
                        return
                elif self.text[self.head] == ' ' and                           \
                                                self.text_color == "\033[0m":
                        self.head += 1
                        self.head_x += 1
                elif self.text[self.head] == '\n':
                        self.head += 1
                        self.head_x = 0
                        self.head_y += 1
                        if self.head_y > 3:
                                self.head_y = 0
                                if self.tail_y <= 0:
                                        self.tail_y = -4 # So that (tail_y+1)%4 == 1
                                        print_loc(' ' * 80, self.y, self.x)
                elif self.text[self.head] == '[':
                        self.text_color = "\033[0;96;4m"
                        print self.text_color
                        self.head += 1
                elif self.text[self.head] == ']':
                        self.text_color = "\033[0m"
                        print self.text_color
                        self.head += 1
                else:
                        print_loc(self.text_color + self.text[self.head],      \
                                                self.y + self.head_y,          \
                                                self.x + self.head_x,)
                        self.head += 1
                        self.head_x += 1
                        return
                self.head_pass()

        def tail_pass(self):
                if self.locked:
                        return
                self.tail_start_time = time()
                if self.tail >= self.length:
                        pass
                elif self.text[self.tail] == '\n':
                        self.tail += 1
                        self.tail_x = 0
                        self.tail_y = (self.tail_y + 1) % 4
                elif match('\[|\]', self.text[self.tail]):
                        self.tail += 1
                elif self.tail_y < 0:
                        self.tail += 1
                else:
                        whitespace = ' ' * (self.tail_x+1)
                        print "\033[0m"
                        print_loc(whitespace, self.y+self.tail_y, self.x)
                        self.tail += 1
                        self.tail_x += 1

        def onKeyPress(self):
                """ Get a character and change user input line accordingly.

                """
                ch = read(fd, 4)
                if ch == '\033':                        # escape
                        self.pause()
                elif '\033' in ch:
                        return
                elif '\t' in ch:                        # tab
                        return
                elif len(self.user_input) >= 80:        # too long
                        self.user_input[:80]
                        return
                elif ch == '\r':                        # return
                        if self.user_input == "":
                                return
                        command = command_list.match(self.user_input)
                        if not command:
                                pass
                        elif command.group(1):
                                self._save(0)
                        elif command.group(2):
                                self._save()
                        elif command.group(3):
                                self._save(command.group(4))
                        link = self.links.match(self.user_input.lower())
                        if link:
                                self.reset(link.group(0))
                        self.user_input = ""
                        self.locked += 1
                        print '\033[0m'
                        print_loc(' '*80, self.y+5, self.x+2)
                        #print_loc(' '*80, self.y+6, 0)
                        self.locked -= 1
                elif ch == '\x7f':                      # backspace
                        if self.user_input == "":
                                return
                        self.user_input = self.user_input[:-1]
                elif ch == ' ':                         # space
                        if self.user_input == "":
                                return
                        elif self.user_input[-1] == ' ':
                                return
                        self.user_input += ' '
                else:                                   # all else
                        self.user_input += ch
                self.locked += 1
                # Highlight valid user input
                if self.links.match(self.user_input.lower()):
                        print '\033[0;96;4m'
                        print_loc(self.user_input+'\033[0;1m < \033[0m ', self.y + 5, self.x)
                elif command_list.match(self.user_input):
                        print '\033[0;1;92m'
                        print_loc(self.user_input+'\033[0;1m < \033[0m ', self.y + 5, self.x)
                else:
                        print '\033[0m'
                        # Display new user input line
                        print_loc(self.user_input+'\033[0;7m \033[0m  ', self.y + 5, self.x)
                self.locked -= 1

        def display(self):
                self._print_box()
                print '\033[0m'
                print '\033[1m'
                if self.x >= 3:
                        print_loc('# \033[0;7m \033[0m', self.y+5, self.x-2)
                else:
                        print_loc('\033[0;7m \033[0m', self.y+5, self.x)
                print '\033[0;1m'
                print_loc('Commands:',                 2,  2)
                print_loc('Key commands:',             2, 60)
                print '\033[0;1;92m'
                print_loc('end game stint',            3,  2)
                print_loc('spare',                     4,  2)
                print_loc('spare as [filename]',       5,  2)
                print '\033[0;96;4m'
                print_loc('link',                      6,  2)
                print '\033[0m'
                print_loc('quit without saving',       3, 28)
                print_loc('save and quit',             4, 28)
                print_loc('save to filename and quit', 5, 28)
                print_loc('inquire about link',        6, 28)
                print_loc('[ESC] - pause game',        3, 60)

        def pause(self):
                self.locked += 1
                pause_start = time()
                print '\033[0m'
                if self.x >= 3:
                        print_loc(v_bar + ' ' * 82 + v_bar, self.y,   self.x-2)
                        print_loc(v_bar + ' ' * 82 + v_bar, self.y+1, self.x-2)
                        print_loc(v_bar + ' ' * 82 + v_bar, self.y+2, self.x-2)
                        print_loc(v_bar + ' ' * 82 + v_bar, self.y+3, self.x-2)
                else:
                        print_loc(' ' * (80+self.x-1), self.y,   self.x-1)
                        print_loc(' ' * (80+self.x-1), self.y+1, self.x-1)
                        print_loc(' ' * (80+self.x-1), self.y+2, self.x-1)
                        print_loc(' ' * (80+self.x-1), self.y+3, self.x-1)
                print '\033[1m'
                print_loc('PAUSE', self.y+1, self.x+37)
                print '\033[0m'
                print_loc('e - end game stint' + ' ' * 8 + '[space] - continue'\
                                               + ' ' * 8 + 's - spare',        \
                                               self.y+2, self.x+8)
                while True:
                        ch = read(fd, 4)
                        if ch == 's':
                                self._save()
                        elif ch == 'e':
                                self._save(0)
                        elif ch == ' ':
                                break
                stty_check()
                print_loc('     ',   self.y+1, self.x+37)
                print_loc(' ' * 61,  self.y+2, self.x+8)
                tmp = prompt("",(self.y, self.x))
                tmp.text = self.text
                tmp.length = self.length
                tmp.head = self.tail
                tmp.head_x = self.tail_x
                tmp.head_y = self.tail_y
                while tmp.head < self.head:
                        tmp.head_pass()
                self.prompt_time += (time() - pause_start)
                self.locked -= 1

        def reset(self, link):
                self.locked += 1
                self._load_text(link)
                self.length = len(self.text)
                self._generate_links()
                self.head       = 0
                self.head_x     = 0
                self.head_y     = 0
                self.tail       = 0
                self.tail_x     = 0
                self.tail_y     = 0
                self.text_color = '\033[0m'
                self.user_input = ""
                self.prompt_time = time()
                self.head_start_time = 0
                self.tail_start_time = 0
                self.display()
                self.locked -= 1
                return

        def _generate_links(self):
                """ Find links and make them a regular expression.

                """
                index = 0
                links = ""
                for ch in self.text:
                        if ch == '[':
                                links += "(^"
                        elif ch == ']':
                                links += ")$|"
                                index += 1
                        elif links[-1:] != '|' and links != "":
                                links += ch
                self.links = compile(links[:-1].lower())

        def _print_box(self):
                # Prompt box
                print '\033[0m'
                if self.x < 3:
                        print_loc(h_bar * (80+self.x), self.y-1, 0)
                        print_loc(' '   * (80+self.x), self.y,   0)
                        print_loc(' '   * (80+self.x), self.y+1, 0)
                        print_loc(' '   * (80+self.x), self.y+2, 0)
                        print_loc(' '   * (80+self.x), self.y+3, 0)
                        print_loc(h_bar * (80+self.x), self.y+4, 0)
                else:
                        print_loc(tl_corner + h_bar * 82 + tr_corner, self.y-1, self.x-2)
                        print_loc(v_bar     + ' '   * 82 + v_bar,     self.y,   self.x-2)
                        print_loc(v_bar     + ' '   * 82 + v_bar,     self.y+1, self.x-2)
                        print_loc(v_bar     + ' '   * 82 + v_bar,     self.y+2, self.x-2)
                        print_loc(v_bar     + ' '   * 82 + v_bar,     self.y+3, self.x-2)
                        print_loc(bl_corner + h_bar * 82 + br_corner, self.y+4, self.x-2)

        def _load_text(self, link):
                if link == "":
                        return
                filename = 'data/'+'_'.join(link.split(' '))
                with open(filename, 'r') as f:
                        self.text = f.read()

        def _save(self, filename = str(int(time()))):
                """ Save data to file, set attribute prompt_time to 0 and exit()

                """
                if filename:
                        with open(filename, 'w') as f:
                                f.write('null')
                self.prompt_time = 0
                exit()
