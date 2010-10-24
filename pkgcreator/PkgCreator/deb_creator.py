#!/usr/bin/python3
#@TODO: Validate file before

import os
import shutil
import yaml
from builder.menu_creator import MenuCreator
from builder.icon_creator import IconCreator

class AbstractGenerator(object):
    def __init__(self, path='package.yaml', outputdir='dist'):
        self.outputdir = outputdir
        self.path = path
        self.has_icon = False
        self.info = {}
    def parse_pkg_markup(self):
        with open(self.path) as f:
            self.info = yaml.load(f)
        #validate file here
        self.has_icon = self.info['general'].has_key('icon')
        if(self.has_icon):
            self.menu_creator = MenuCreator(self.info['general'])
            self.icon_creator = IconCreator(self.info['general'])

class DebianGenerator(AbstractGenerator):
    def __init__(self, path, outputdir):
        super().__init__(path, outputdir)
        self.outputdir = os.path.join(self.outputdir, 'deb')
    def create_package(self):
        #Creating install files
        for f in self.info['files']:
            src = f['src']
            dst = os.path.join(self.outputdir, f['dst'][1:])
            try:
                os.makedirs(os.path.dirname(dst))
                shutil.copy(src, dst)
            except OSError:
                pass
        #Creating menu entries
        #Creating icons
        #Creating Debian-related files

if __name__ == '__main__':
    g = DebianGenerator()
    g.create_package()