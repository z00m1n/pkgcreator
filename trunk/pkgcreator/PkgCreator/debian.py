#!/usr/bin/python3
#@TODO: Validate file before

import os
import shutil
import yaml
from PkgCreator.menu_creator import MenuCreator
from PkgCreator.icon_creator import IconCreator

class AbstractGenerator(object):
    def __init__(self, pkg_markup='package.yaml', outputdir='dist'):
        self.outputdir = outputdir
        self.pkg_markup = pkg_markup
        self.has_icon = False
        self.info = {}
    def parse_pkg_markup(self):
        with open(self.pkg_markup) as f:
            self.info = yaml.load(f)
        #validate file here
        if 'menu' in self.info.keys():
            self.menu_creator = MenuCreator(self.info)
            if 'icon' in self.info['menu'].keys():
                self.icon_creator = IconCreator(self.info['menu']['icon'])
        else:
            self.menu_creator = self.icon_creator = None

class DebianGenerator(AbstractGenerator):
    def __init__(self, pkg_markup, outputdir):
        super().__init__(pkg_markup, outputdir)
        self.outputdir = os.path.join(self.outputdir, 'deb')
    def __copy_file(self, src, dst):
        try:
            os.makedirs(os.path.dirname(dst))
            shutil.copy(src, dst)
        except OSError: #folder already exists
            pass
    def __create_file(self, path, content):
        try:
            os.makedirs(os.path.dirname(dst))
            with open(path, 'w') as f:
                f.write(content)
        except OSError: #folder already exists
            pass
    def create_package(self):
        #Install files
        for f in self.info['files']:
            src = f['src']
            dst = os.path.join(self.outputdir, f['dst'][1:])
            self.__copy_file(src, dst)
            print (' - Copying %s to %s ...' % (src, dst))
        #Menus and icons
        if self.has_menu:
            menus = self.menu_creator.create()
            for m in menus:
                path = os.path.join(self.outputdir, m['path'])
                self.__create_file(path, m['content'])
        if 'icon' in self.info['menu'].keys():
            icons = self.icons_creator.create()
        #Creating Debian-related files
        #wow, later guy!
        #Running dpkg
        #Buying pizza

if __name__ == '__main__':
    g = DebianGenerator()
    g.create_package()