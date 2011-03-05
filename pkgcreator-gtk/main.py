#!/usr/bin/env python
import sys
from PkgCreatorGtk.gui import GUI

def main():
    #TODO: Get command line argument to eventually open a file
    gui = GUI()
    gui.show()

if __name__ == '__main__':
    main()
    sys.exit(0)
