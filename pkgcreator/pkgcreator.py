#!/usr/bin/env python

import argparse
import sys
from PkgCreator.debian import DebianGenerator

def main():
    parser = argparse.ArgumentParser(description='Creates binaries packages.',
        epilog="Currently only Debian packages are generated."
    )
    parser.add_argument('--outputdir', nargs=1, default='dist',
        help='sets output dir for generated packages.'
    )
    parser.add_argument('-c', '--color', action='store_true', help='color output.')
    parser.add_argument('yaml_file', help='specifies the package markup file.')
    args = parser.parse_args()
    d = DebianGenerator(args.yaml_file, args.outputdir, args.color)
    d.parse_pkg_markup()
    d.create_package()
    sys.exit(0)

if __name__ == '__main__':
    main()
