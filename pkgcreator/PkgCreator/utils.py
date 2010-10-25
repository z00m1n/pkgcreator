import os
from os import path
import shutil
import md5
from PkgCreator.console import extended_print

__all__ = [
    'camel_case', 'create_path', 'copy_file', 'create_file',
    'calculate_md5sums', 'calculate_size'
]

def camel_case(string):
    return string.replace('_', ' ').title().replace(' ', '')

def create_path(dirpath):
    try:
        os.makedirs(dirpath)
    except OSError:
        pass

def copy_file(src, dst):
    create_path(path.dirname(dst))
    msg = '- Copying %s to %s ...' % (src, dst)
    extended_print(msg, indent=1)
    try:
        shutil.copy(src, dst)
    except IOError:
        msg = '* Error while copying %s!' % src
        extended_print(msg, indent=2, flags='red,bold')

def create_file(dirpath, content):
    create_path(path.dirname(dirpath))
    msg = '- Creating %s ...' % dirpath
    extended_print(msg, indent=1)
    try:
        with open(dirpath, 'w') as f:
            f.write(content)
    except IOError:
        msg = '* Error while creating %s!' % dirpath
        extended_print(msg, indent=2, flags='red,bold')

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
                filemd5 = md5.new(filecontent)
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