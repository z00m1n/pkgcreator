import os
import yaml
from PkgCreator.console import extended_print
from PkgCreator.menu_creator import MenuCreator
from PkgCreator.icon_creator import IconCreator

MSG_INSTALL = 'Copying install files'
MSG_MENUS = 'Generating menu entries'
MSG_ICONS = 'Generating icons'
MSG_PACKAGING = 'Creating final package'

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
                self.icon_creator = IconCreator (
                    self.info['menu']['icon'],
                    self.info['general']['package_name']
                )
        else:
            self.menu_creator = self.icon_creator = None
    def title(self, msg):
        extended_print(msg, flags='bold', fill_up='=', fill_down='=')
    def end_message(self, success):
        msg = 'End of execution'
        if success:
            extended_print(msg, flags='blue,bold', center_width=80, center_char='*')
        else:
            extended_print(msg, flags='red,bold', center_width=80, center_char='*')



