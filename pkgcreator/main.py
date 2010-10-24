#!/usr/bin/python3

from PkgCreator.deb_creator import DebCreator

if __name__ == '__main__':
    d = DebCreator(outputdir='dist', path='example/package.yaml')
    d.parse_pkg_markup()
    d.create_package()
