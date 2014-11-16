#-------------------------------------------------------------------------------
# Support library for the game
#-------------------------------------------------------------------------------

from time import time
from re import compile, match

command_list = compile('(^forsake game stint)\s*$|(^spare)\s*$|(^spare as )(\w+)\s*$')

def print_loc(text, y, x):
        print("\033[%s;%sH" % (y,x) + text)

def getch():
        import tty, termios, sys
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
        finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def save(filename = str(int(time()))):
        with open(filename, 'w') as f:
                f.write('null')
        exit()

class prompt(object):
        def __init__(self, y, x, text, start_head = 0, start_tail = 5):
                self.prompt_time = time()
                self.head_start_time = 0
                self.tail_start_time = 0
                self.text = text
                self.length = len(text)
                index = 0
                self.links = []
                for ch in text:
                        if ch == '[':
                                self.links.append("")
                        elif ch == ']':
                                index += 1
                        elif len(self.links) > index:
                                self.links[index] += ch
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

        def head_pass(self):
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
                self.tail_start_time = time()
                if self.tail > 80*self.lines:
                        pass
                elif self.tail_x >= 80:
                        self.tail += 1
                        self.tail_x = 0
                        self.tail_y += 1
                else:
                        print_loc("\033[0m ", self.y + self.tail_y, self.x + self.tail_x)
                        self.tail += 1
                        self.tail_x += 1

        def onKeyPress(self):
                """ Get a character and change user input line accordingly.

                """
                ch = getch()
                if ch == '\x1b':                        # escape
                        exit()
                if ch == '\r':                          # return
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
                        self.user_input = ""
                        print '\033[0m'
                        print_loc(' '*80, self.y+5, self.x+2)
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
                # Highlight valid user input
                if self.user_input.lower() in self.links:
                        print self.user_input.lower()
                        print '\033[0m\033[96m\033[4m'
                elif command_list.match(self.user_input):
                        print '\033[0m\033[1m\033[92m'
                else:
                        print '\033[0m'
                # Display new user input line
                print_loc(self.user_input+'\033[0m\033[1m < ', self.y + 5, self.x)

        def display(self):
                # Prompt box
                print '\033[4m'
                print '\033[1m'
                print_loc(' '*82, self.y-1, self.x-1)
                print_loc('Old man', self.y-1, self.x)
                print '\033[0m'
                print '\033[1m'
                print_loc('|',  self.y, self.x-2)
                print_loc('|',  self.y, self.x+81)
                print_loc('|',  self.y+1, self.x-2)
                print_loc('|',  self.y+1, self.x+81)
                print_loc('|',  self.y+2, self.x-2)
                print_loc('|',  self.y+2, self.x+81)
                print_loc('|',  self.y+3, self.x-2)
                print_loc('|',  self.y+3, self.x+81)
                print_loc('|',  self.y+4, self.x-2)
                print_loc('|',  self.y+4, self.x+81)
                print '\033[4m'
                print_loc(' '*82, self.y+4, self.x-1)
                print '\033[0m'
                print '\033[1m'
                print_loc('>  <', self.y+5, self.x-2)
                print '\033[0m'
                print_loc('\033[1mCommands:\033[0m', 10, 20)
                print '\033[0m\033[1m\033[92m'
                print_loc('forsake game stint', 11, 20)
                print_loc('spare', 12, 20)
                print_loc('spare as [filename]', 13, 20)
                print '\033[0m'
                print_loc('quit without saving', 11, 48)
                print_loc('save and quit', 12, 48)
                print_loc('save to filename and quit', 13, 48)

        def pause(self):
                print_loc('Press a key to start', self.y+2, self.x+30)
                getch()
                print_loc('                    ', self.y+2, self.x+30)
                self.prompt_time = time()
