#@TODO: Support for html parsing!!

import sys

try:
    from colorama import init, Fore, Back, Style
    colorama = True
except ImportError:
    colorama = False

__all__ = ["console"]


class Console:
    def __init__(self):
        self.reset()
        self.color = False
    def set_color(self, color):
        self.color = color
        if colorama and color:
            init(autoreset=True)
    def reset(self):
        self.indent = 0
        self.flags = ''
        self.fill_up = ''
        self.fill_down = ''
        self.center_width = False
        self.center_char = ' '
    def eprint(self, msg, indent=0, flags='', fill_up=None, fill_down=None,
               center_width=False, center_char=' ', end="\n"):
        """Prints a message to stdout with many coloring and style options.
            msg: message to print
            indent: insert spaces before the beginning
            flags: bold, light, red
            fill_up: char to use to create a bar above the string
            fill_down: char to use to create a bar below the string
            center_width, center_char: see center method of strings - help("".center)
            end: string to append before printing (see python3 print function)
        """
        if indent:
            msg = (' ' * 4 * indent) + msg
        elif self.indent:
            msg = (' ' * 4 * self.indent) + msg
        size = len(msg)
        if center_width:
            msg = msg.center(center_width, center_char)
        elif self.center_width:
            if center_char:
                msg = msg.center(self.center_width, center_char)
            else:
                msg = msg.center(self.center_width, self.center_char)
        if fill_up:
            title = (fill_up * size) + "\n"
            msg = title + msg
        elif self.fill_up:
            title = (self.fill_up * size) + "\n"
            msg = title + msg
        if fill_down:
            title = "\n" + (fill_down * size)
            msg += title
        elif self.fill_down:
            title = "\n" + (self.fill_down * size)
            msg += title
        if colorama and self.color:
            allflags = flags + self.flags
            if 'bold' in allflags:
                msg = Style.BRIGHT + msg
            if 'light' in allflags:
                msg = Style.DIM + msg
            if 'red' in allflags:
                msg = Fore.RED + msg
            elif 'blue' in allflags:
                msg = Fore.BLUE + msg
            elif 'green' in allflags:
                msg = Fore.GREEN + msg
            #@TODO: add other flags here
        msg += end
        sys.stdout.write(msg)
        sys.stdout.flush()

console = Console()
