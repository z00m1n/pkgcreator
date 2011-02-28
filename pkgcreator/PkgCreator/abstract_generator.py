import sys
import os
import yaml
from time import time
from console import console as c
from menu_creator import MenuCreator
from icon_creator import IconCreator
from resources import SCHEMA_PATH

MSG_INSTALL = 'Copying install files'
MSG_MENUS = 'Generating menu entries'
MSG_ICONS = 'Generating icons'
MSG_PACKAGING = 'Creating final package'

class AbstractGenerator(object):
    def __init__(self, pkg_markup='package.yaml', outputdir='dist', color=False):
        self.outputdir = outputdir
        self.pkg_markup = pkg_markup
        self.has_icon = False
        self.info = {}
        c.set_color(color)
    def validate(self, path):
        #@todo: verify existence of kwalify
        if not os.path.isfile(path):
            return False
        else:
            log = "/tmp/pkgcreator%s.log" % int(time()*100)
            cmd = "kwalify -f %s %s > %s"
            cmd = cmd % (SCHEMA_PATH, self.pkg_markup, log)
            os.system(cmd)
            os.system("cat %s" % log)
            with open(log) as f:
                contents = f.read()
                if 'INVALID' in contents:
                    return False
                else:
                    return True
    def parse_pkg_markup(self):
        c.title('Validating package markup file...')
        with open(self.pkg_markup) as f:
            try:
                self.info = yaml.load(f)
            except yaml.YAMLError, exc:
                msg = '* YAML parser has found an error: '
                c.eprint(msg, flags='red,bold', indent=1)
                c.indent = 2
                c.flags = 'bold'
                c.eprint('- Context: ' + exc.context)
                c.eprint('- Problem: ' + exc.problem)
                c.eprint('- Where: ' + str(exc.problem_mark).strip())
                c.reset()
                self.quit_with_message(False)
        if(self.validate(self.pkg_markup)):
            c.eprint('* File successfully validated', indent=1, flags='green,bold')
        else:
            c.eprint('* Invalid or inexistent file!', indent=1, flags='red,bold')
            sys.exit(1)
        if 'menu' in self.info.keys():
            self.menu_creator = MenuCreator(self.info)
            if 'icon' in self.info['menu'].keys():
                self.icon_creator = IconCreator (
                    self.info['menu']['icon'],
                    self.info['general']['package_name']
                )
        else:
            self.menu_creator = self.icon_creator = None
    def quit_with_message(self, success):
        msg = 'End of execution'
        if success:
            c.eprint(msg, flags='blue,bold', center_width=80, center_char='*')
            sys.exit(0)
        else:
            c.eprint(msg, flags='red,bold', center_width=80, center_char='*')
            sys.exit(1)



