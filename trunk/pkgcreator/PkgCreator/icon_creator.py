import os.path
from PIL import Image


#@TODO: Add support to SVG: /usr/share/icons/hicolor/scalable/apps
#PIL doesn't support SVG yet. PythonMagick poor documented.

PIXMAP = 'usr/share/pixmaps/%s.xpm'
PNG = 'usr/share/icons/hicolor/%sx%s/apps/%s.png'
SIZES = (16,22,24,32,36,48,64,72,96,128,192)

class IconCreator(object):
    def __init__(self, iconpath, package_name):
        self.path = iconpath
        self.package_name = package_name
    def create(self):
        if not self.path:
            return
        icons = []
        self.icon = Image.open(self.path)
        """Creating pixmap... PIL doesn't support XPM creation
        #print(' - Creating pixmap icon...')
        #path = PIXMAP % self.package_name
        #img = self.icon.resize((32,32))
        icons.append({'path': path, 'img': img})"""
        #Creating PNGs
        for s in SIZES:
            path = PNG % (s, s, self.package_name)
            img = self.icon.resize((s,s))
            icons.append({'path': path, 'img': img})
        return icons
