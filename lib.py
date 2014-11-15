#-------------------------------------------------------------------------------
# Support library for the game
#-------------------------------------------------------------------------------

from time import time

def print_loc(text, y, x):
        print("\033[%s;%sH" % (y,x) + text)

class prompt(object):
        def __init__(self, text, start_head = 0, start_tail = 5):
                self.prompt_time = time()
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
                self.head       = 0
                self.head_x     = 0
                self.head_y     = 0
                self.tail       = 0
                self.tail_x     = 0
                self.tail_y     = 0
                self.text_color = '\033[0m'

        def head_pass(self, y, x):
                if self.head >= self.length:
                        pass
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
                                                y + self.head_y,               \
                                                x + self.head_x,)
                        self.head += 1
                        self.head_x += 1
                        return True
                return False

        def head_tail(self, y, x):
                if self.tail < 80*self.lines:
                        pass
                elif self.tail_x >= 80:
                        tail += 1
                        tail_x = 0
                        tail_y += 1
                else:
                        print_loc("\033[0m ", 60 + tail_x, 20 + tail_y)
                        tail += 1
                        tail_x += 1
