import os
import yaml
from PkgCreator.console import console as c
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
            try:
                self.info = yaml.load(f)
            except yaml.YAMLError, exc:
                msg = 'YAML parser has found an error: '
                c.eprint(msg, flags='red,bold')
                msg = '- Context: ' + exc.context + '\n'
                msg += '- Problem: ' + exc.problem + '\n'
                msg += '- Where: ' + str(exc.problem_mark).strip()
                c.eprint(msg, flags='bold', indent=1)
                self.quit_with_message(False)
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
        c.eprint(msg, flags='bold', fill_up='=', fill_down='=')
    def quit_with_message(self, success):
        msg = 'End of execution'
        if success:
            c.eprint(msg, flags='blue,bold', center_width=80, center_char='*')
        else:
            c.eprint(msg, flags='red,bold', center_width=80, center_char='*')



