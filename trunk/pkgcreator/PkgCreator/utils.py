import os
import shutil
from PkgCreator.console import extended_print

def camel_case(string):
    return string.replace('_', ' ').title().replace(' ', '')

def create_path(path):
    try:
        os.makedirs(path)
    except OSError:
        pass

def copy_file(src, dst):
    create_path(os.path.dirname(dst))
    msg = '- Copying %s to %s ...' % (src, dst)
    extended_print(msg, indent=1)
    try:
        shutil.copy(src, dst)
    except IOError:
        msg = '* Error while copying %s!' % src
        extended_print(msg, indent=2, flags='red,bold')

def create_file(path, content):
    create_path(os.path.dirname(path))
    msg = '- Creating %s ...' % path
    extended_print(msg, indent=1)
    try:
        with open(path, 'w') as f:
            f.write(content)
    except IOError:
        msg = '* Error while creating %s!' % path
        extended_print(msg, indent=2, flags='red,bold')
