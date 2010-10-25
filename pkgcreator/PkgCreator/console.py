#@TODO: Support for html parsing!!

__all__ = ["console"]

try:
    from colorama import init, Fore, Back, Style
    colorama = True
except ImportError:
    colorama = False

if colorama:
    init(autoreset=True)

class Console:
    def __init__(self):
        self.reset()
    def reset(self):
        self.indent = 0
        self.flags = ''
        self.fill_up = ''
        self.fill_down = ''
        self.center_width = False
        self.center_char = ' '
    def eprint(msg, indent=0, flags='', fill_up=None, fill_down=None,
               center_width=False, center_char=' '):
        """Prints a message to stdout with many coloring and style options.
            msg: message to print
            indent_level: insert spaces before the beginning
            flags: bold, light, red
            fill_up: char to use to create a bar above the string
            fill_down: char to use to create a bar below the string
            center_width, center_char: see center method of strings - help("".center)
        """
        msg = (' ' * 4 * indent) + msg
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
        if colorama:
            allflags = flags.extend(self.flags)
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
        print msg

console = Console()