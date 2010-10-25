import os

DEBUG = False

SCHEMA_FILENAME = 'package_schema.yaml'
if DEBUG:
    SCHEMA_DIRNAME = 'data/'
else:
    SCHEMA_DIRNAME = '/usr/share/pkgcreator'

SCHEMA_PATH = os.path.join(SCHEMA_DIRNAME, SCHEMA_FILENAME)