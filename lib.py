#-------------------------------------------------------------------------------
# Support library for the game
#-------------------------------------------------------------------------------

class prompt(object):
        def __init__(self, text):
                self.text = text
                index = 0
                self.links = []
                for ch in text:
                        if ch == '[':
                                self.links.append("")
                        elif ch == ']':
                                index += 1
                        elif len(self.links) > index:
                                self.links[index] += ch
