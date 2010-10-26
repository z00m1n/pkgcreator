from distutils.core import setup

version = '0.1'

setup (
       name = 'pkgcreator',
       version = version,
       description = 'Creates Debian binary packages',
       author='Leandro Resende Mattioli',
       author_email='leandro.mattioli@gmail.com',
       url='http://code.google.com/p/pkgcreator',
       requires = ['gtk', 'yaml', 'PIL'],
       scripts = ['pkgcreator.py'],
       data_files= [('/usr/share/pkgcreator', ['data/package_schema.yaml'])],
       packages = ['PkgCreator']
)
