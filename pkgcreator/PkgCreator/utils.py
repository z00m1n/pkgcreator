import os
import shutil

def camel_case(string):
    return string.replace('_', ' ').title().replace(' ', '')

def copy_file(src, dst):
    try:
        os.makedirs(os.path.dirname(dst))
    except OSError: #folder already exists
        pass
    finally:
        print (' - Copying %s to %s ...' % (src, dst))
        #shutil.copy(src, dst)

def create_file(path, content):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass
    finally:
        print (' - Creating %s ...' % path)
        #with open(path, 'w') as f:
        #    f.write(content)
