#-------------------------------------------------------------------------------
# Support library for the game
#-------------------------------------------------------------------------------

from time import time
from re import compile, match, sub
import sys

command_list = compile('(^end game stint)\s*$|(^spare)\s*$|(^spare as )(\w+)\s*$')

v_bar = b'\xe2\x94\x82'
h_bar = b'\xe2\x94\x80'
bl_corner = b'\xe2\x95\xb0'
br_corner = b'\xe2\x95\xaf'
tl_corner = b'\xe2\x95\xad'
tr_corner = b'\xe2\x95\xae'
bl_square_corner = b'\xe2\x94\x94'

def print_loc(text, y, x):
        print("\033[%s;%sH" % (y,x) + text)

def save(filename = str(int(time()))):
        with open(filename, 'w') as f:
                f.write('null')
        exit()

class prompt(object):
        def __init__(self, y, x, text, start_head = 0, start_tail = 5):
                self.text = text
                self.length = len(self.text)
                self.links = ""
                self._generate_links()
                self.lines = len(self.text.split('\n'))
                self.y          = y
                self.x          = x
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
                print_loc(str(self.head)+ "  ",   2, 86)
                print_loc(str(self.head_x)+ "  ", 3, 86)
                print_loc(str(self.head_y)+ "  ", 4, 86)
                print_loc(str(self.tail)+ "  ",   5, 86)
                print_loc(str(self.tail_x)+ "  ", 6, 86)
                print_loc(str(self.tail_y)+ "  ", 7, 86)
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
                        self.text_color = "\033[0m\033[96m\033[4m"
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
                ch = sys.stdin.read(1)
                if ch == '\x1b':                        # escape
                        self.pause()
                elif ch == '\r':                          # return
                        if self.user_input == "":
                                return
                        command = command_list.match(self.user_input)
                        if not command:
                                pass
                        elif command.group(1):
                                exit()
                        elif command.group(2):
                                save()
                        elif command.group(3):
                                save(command.group(4))
                        link = self.links.match(self.user_input.lower())
                        if not link:
                                pass
                        else:
                                self.reset(link.group(0))
                        self.user_input = ""
                        self.locked += 1
                        print '\033[0m'
                        print_loc(' '*80, self.y+5, self.x+2)
                        self.locked -= 1
                elif ch == '\x7f':                      # backspace
                        if self.user_input == "":
                                return
                        self.user_input = self.user_input[:-1]
                elif ch == ' ':                         # space
                        if self.user_input == "":
                                return
                        self.user_input += ' '
                elif len(self.user_input) >= 80:        # too long
                        return
                else:                                   # all else
                        self.user_input += ch
                self.locked += 1
                # Highlight valid user input
                if self.links.match(self.user_input.lower()):
                        print '\033[0m\033[96m\033[4m'
                elif command_list.match(self.user_input):
                        print '\033[0m\033[1m\033[92m'
                else:
                        print '\033[0m'
                # Display new user input line
                print_loc(self.user_input+'\033[0m\033[1m < ', self.y + 5, self.x)
                self.locked -= 1

        def display(self):
                self._print_box()
                print '\033[0m'
                print '\033[1m'
                print_loc('>  <', self.y+5, self.x-2)
                print '\033[0m'
                print_loc('\033[1mCommands:\033[0m',   2, 2)
                print '\033[0m\033[1m\033[92m'
                print_loc('end game stint',            3, 2)
                print_loc('spare',                     4, 2)
                print_loc('spare as [filename]',       5, 2)
                print '\033[0m\033[96m\033[4m'
                print_loc('link',                      6, 2)
                print '\033[0m'
                print_loc('quit without saving',       3, 28)
                print_loc('save and quit',             4, 28)
                print_loc('save to filename and quit', 5, 28)
                print_loc('inquire about link',        6, 28)

        def pause(self):
                self.locked += 1
                pause_start = time()
                print '\033[0m'
                print_loc(v_bar+' ' * 82+v_bar,       self.y,   self.x-2)
                print_loc(v_bar+' ' * 82+v_bar,       self.y+1, self.x-2)
                print_loc(v_bar+' ' * 82+v_bar,       self.y+2, self.x-2)
                print_loc(v_bar+' ' * 82+v_bar,       self.y+3, self.x-2)
                print '\033[1m'
                print_loc('PAUSE',                self.y+1, self.x+37)
                print '\033[0m'
                print_loc('e - end game stint'+' '*8+'[space] - continue'+' '*8+'s - spare', self.y+2, self.x+8)
                ch = sys.stdin.read(1)
                if ch == '[':
                        ch = sys.stdin.read(1)
                elif ch == 's':
                        save()
                elif ch == 'e':
                        exit()
                elif ch == ' ':
                        print_loc('     ', self.y+1, self.x+37)
                        print_loc(' '*61, self.y+2, self.x+8)
                        tmp = prompt(self.y, self.x, self.text)
                        tmp.head = self.tail
                        tmp.head_x = self.tail_x
                        tmp.head_y = self.tail_y
                        while tmp.head < self.head:
                                tmp.head_pass()
                else:
                        self.pause()
                self.prompt_time += (time() - pause_start)
                self.locked -= 1

        def reset(self, link):
                self.locked += 1
                filename = 'data/'+'_'.join(link.split(' '))
                with open(filename, 'r') as f:
                        self.text = f.read()
                self.length = len(self.text)
                self._generate_links()
                self.lines = len(self.text.split('\n'))
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
                                links += ")\s*$|"
                                index += 1
                        elif links[-1:] != '|' and links != "":
                                links += ch
                self.links = compile(links[:-1].lower())

        def _print_box(self):
                # Prompt box
                print '\033[0m'
                print_loc(tl_corner+h_bar*9+tr_corner,  self.y-2, self.x-2)
                print_loc(v_bar,                        self.y-1, self.x-2)
                print_loc(tr_corner,                    self.y-1, self.x+81)
                print_loc(bl_square_corner+h_bar*72,    self.y-1, self.x+8)
                print_loc(bl_corner,                    self.y+4, self.x-2)
                print_loc(br_corner,                    self.y+4, self.x+81)
                print_loc(h_bar*82,                     self.y+4, self.x-1)
                print_loc(v_bar+' ' * 82+v_bar,       self.y,   self.x-2)
                print_loc(v_bar+' ' * 82+v_bar,       self.y+1, self.x-2)
                print_loc(v_bar+' ' * 82+v_bar,       self.y+2, self.x-2)
                print_loc(v_bar+' ' * 82+v_bar,       self.y+3, self.x-2)
                print '\033[0m'
                print '\033[4m'
                print '\033[1m'
                print_loc('Old man', self.y-1, self.x)
