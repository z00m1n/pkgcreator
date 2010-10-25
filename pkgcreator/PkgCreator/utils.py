import os
from os import path
import shutil
import hashlib
from glob import glob
from PkgCreator.console import console as c

__all__ = [
    'camel_case', 'create_path', 'copy_file', 'create_file',
    'calculate_md5sums', 'calculate_size', 'VERBOSE'
]

VERBOSE = True

def camel_case(string):
    return string.replace('_', ' ').title().replace(' ', '')

def create_path(dirpath):
    try:
        os.makedirs(dirpath)
    except OSError:
        pass

def copy_file(src, dst):
    create_path(path.dirname(dst))
    for i in glob(src):
        if VERBOSE:
            msg = '- Copying %s to %s ... ' % (i, dst)
            c.eprint(msg, indent=1, end='')
        try:
            shutil.copy(i, dst)
            if VERBOSE:
                c.eprint('[OK]', flags='green,bold')
        except IOError:
            if VERBOSE:
                c.eprint('[FAIL]', flags='red,bold')

def create_file(dirpath, content):
    create_path(path.dirname(dirpath))
    if VERBOSE:
        msg = '- Creating %s ...' % dirpath
        c.eprint(msg, indent=1, end='')
    try:
        with open(dirpath, 'w') as f:
            f.write(content)
        if VERBOSE:
            c.eprint('[OK]', flags='green,bold')
        return True
    except IOError:
        if VERBOSE:
            c.eprint('[FAIL]', flags='red,bold')
        return False

def calculate_md5sums(dirpath, ignore_list):
    content = ''
    for root, dirs, files in os.walk(dirpath):
        for i in ignore_list:
            if i in dirs:
                dirs.remove(i)
        for name in files:
            filepath = path.join(root, name)
            with open(filepath) as f:
                filecontent = f.read()
                filemd5 = hashlib.md5()
                filemd5.update(filecontent)
                content += filemd5.hexdigest() + ' ' + filepath + "\n"
            content.strip()
    return content

def calculate_size(dirpath, ignore_list):
    total_size = 0
    for root, dirs, files in os.walk(dirpath):
        if ignore_list:
            for i in ignore_list:
                if i in dirs:
                    dirs.remove(i)
        total_size += sum(path.getsize(path.join(root, name)) for name in files)
    return total_size