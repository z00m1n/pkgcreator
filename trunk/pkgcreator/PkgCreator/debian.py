#!/usr/bin/env python
#@TODO: Validate file before

import os
from PkgCreator import utils
from PkgCreator.console import extended_print
from PkgCreator.abstract_generator import AbstractGenerator

class DebianGenerator(AbstractGenerator):
    def __init__(self, pkg_markup, outputdir):
        AbstractGenerator.__init__(self, pkg_markup, outputdir)
        self.outputdir = os.path.join(self.outputdir, 'deb')
    def create_package(self):
        #Install files
        self.msg_install()
        for f in self.info['files']:
            src = f['src']
            dst = os.path.join(self.outputdir, f['dst'][1:])
            utils.copy_file(src, dst)
        #Menus and icons
        if 'menu' in self.info.keys():
            self.msg_menus()
            menus = self.menu_creator.create()
            for m in menus:
                path = os.path.join(self.outputdir, m['path'])
                utils.create_file(path, m['content'])
        if 'icon' in self.info['menu'].keys():
            self.msg_icons()
            icons = self.icon_creator.create()
            for i in icons:
                path = os.path.join(self.outputdir, i['path'])
                extended_print('- Creating icon %s ...' % path, indent=1)
                utils.create_path(path)
                i['img'].save(path)
        #Creating Debian-related files


if __name__ == '__main__':
    g = DebianGenerator()
    g.create_package()