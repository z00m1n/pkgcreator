import os
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
                self.icon_creator = IconCreator (
                    self.info['menu']['icon'],
                    self.info['general']['package_name']
                )
        else:
            self.menu_creator = self.icon_creator = None