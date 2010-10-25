#@TODO: Support for html parsing!!

try:
    from colorama import init, Fore, Back, Style
    colorama = True
except ImportError:
    colorama = False

if colorama:
    init(autoreset=True)

def extended_print(msg, indent=0, flags='', fill_up=None, fill_down=None,
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
    if fill_up:
        title = (fill_up * size) + "\n"
        msg = title + msg
    if fill_down:
        title = "\n" + (fill_down * size)
        msg += title
    if colorama:
        if 'bold' in flags:
            msg = Style.BRIGHT + msg
        if 'light' in flags:
            msg = Style.DIM + msg
        if 'red' in flags:
            msg = Fore.RED + msg
        elif 'blue' in flags:
            msg = Fore.BLUE + msg
        elif 'green' in flags:
            msg = Fore.GREEN + msg
        #@TODO: add other flags here
    print msg

