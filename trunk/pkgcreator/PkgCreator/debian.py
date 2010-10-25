#!/usr/bin/env python
#@TODO: Validate file before

import os
from stat import S_IRWXU,  S_IXGRP, S_IRGRP
from PkgCreator import utils
from PkgCreator.console import extended_print
from PkgCreator.abstract_generator import AbstractGenerator
from PkgCreator.abstract_generator import MSG_INSTALL, MSG_MENUS, MSG_ICONS, MSG_PACKAGING
from PkgCreator.menu_creator import POSTINST, POSTRM

class DebianGenerator(AbstractGenerator):
    def __init__(self, pkg_markup, outputdir):
        AbstractGenerator.__init__(self, pkg_markup, outputdir)
        self.outputdir = os.path.join(self.outputdir, 'deb')
        self.debiandir = os.path.join(self.outputdir, 'DEBIAN')
    def create_package(self):
        #Install files
        self.title(MSG_INSTALL)
        for f in self.info['files']:
            src = f['src']
            dst = os.path.join(self.outputdir, f['dst'][1:])
            utils.copy_file(src, dst)
        #Menus
        if 'menu' in self.info.keys():
            self.title(MSG_MENUS)
            menus = self.menu_creator.create()
            for m in menus:
                path = os.path.join(self.outputdir, m['path'])
                utils.create_file(path, m['content'])
        #Icons
        if 'icon' in self.info['menu'].keys():
            self.title(MSG_ICONS)
            icons = self.icon_creator.create()
            for i in icons:
                path = os.path.join(self.outputdir, i['path'])
                extended_print('- Creating icon %s ...' % path, indent=1)
                utils.create_path(os.path.dirname(path))
                i['img'].save(path)
        #Creating Debian-related files
        self.title('Generating Debian stuff')
        if 'menu' in self.info.keys():
            extended_print('- Creating postinst and postrm scripts ...', indent=1)
            postinst = os.path.join(self.debiandir, 'postinst')
            postrm = os.path.join(self.debiandir, 'postrm')
            utils.create_file(postinst, POSTINST)
            utils.create_file(postrm, POSTRM)
            mode = S_IRWXU | S_IXGRP | S_IRGRP
            os.chmod(postinst, mode)
            os.chmod(postrm, mode)
        ignore_list = ['.svn', 'DEBIAN']
        extended_print('- Calculating md5sums ...', indent=1)
        md5sum_path = os.path.join(self.debiandir, 'md5sum')
        md5sum_values = utils.calculate_md5sums(self.outputdir, ignore_list)
        utils.create_file(md5sum_path, md5sum_values)
        extended_print('- Calculating installed size ...', indent=1)
        installed_size = utils.calculate_size(self.outputdir, ignore_list)
        extended_print('- Generating Control file ...', indent=1)
        #TODO
        self.title(MSG_PACKAGING)
        extended_print('- Running dpkg-deb ...', indent=1)
        #TODO

if __name__ == '__main__':
    g = DebianGenerator()
    g.create_package()