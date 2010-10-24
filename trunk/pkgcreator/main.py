#!/usr/bin/env python

from PkgCreator.debian import DebianGenerator

if __name__ == '__main__':
    d = DebianGenerator(outputdir='dist', pkg_markup='example/package.yaml')
    d.parse_pkg_markup()
    d.create_package()
