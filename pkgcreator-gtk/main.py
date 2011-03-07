#!/usr/bin/env python
import sys
import argparse
from PkgCreatorGtk.gui import GUI

def main():
    parser = argparse.ArgumentParser(description='GTK+ pkgcreator YAML files editor.')
    parser.add_argument('yaml_file', 
                        help='specifies the package markup file to be edited.',
                        nargs='?')
    args = parser.parse_args()
    gui = GUI()
    if args.yaml_file:
        gui.load_file(args.yaml_file)
    gui.show()

if __name__ == '__main__':
    main()
    sys.exit(0)
