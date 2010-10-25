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
    parser.add_argument('yaml_file', help='specifies the package markup file.')
    args = parser.parse_args()
    d = DebianGenerator(outputdir=args.outputdir, pkg_markup=args.yaml_file)
    d.parse_pkg_markup()
    d.create_package()
    sys.exit(0)

if __name__ == '__main__':
    main()
