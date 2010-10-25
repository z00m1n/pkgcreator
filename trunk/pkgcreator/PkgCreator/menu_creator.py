import os
from PkgCreator.utils import camel_case
from PkgCreator.console import console as c

#Forbid fields only_show_in and not_show_in simultanealy

APPS_ENTRY_PATH = 'usr/share/applications/%s.desktop'
APP_REG_ENTRY_PATH = 'usr/share/application-registry/%s.applications'
MENU_ENTRY_PATH = 'usr/share/menu/%s'
POSTINST = POSTRM = 'if test -x /usr/bin/update-menus; then update-menus; fi'
FREEDESKTOP_BOOLEAN = {}
for x in ('no_display', 'hidden', 'startup_notify'):
    FREEDESKTOP_BOOLEAN[x] = camel_case(x)
FREEDESKTOP_BOOLEAN['requires_terminal'] = 'Terminal'
FREEDESKTOP_OTHER = {}
for x in (
    'generic_name', 'startup_wm_class', 'comment',
    'only_show_in', 'not_show_in', 'try_exec', 'path', 'categories'
):
    FREEDESKTOP_OTHER[x] = camel_case(x)
FREEDESKTOP_OTHER['mime_types'] = 'MimeType'

class MenuCreator(object):
    def __init__(self, info):
        self.info = info
    def create(self):
        c.flags = 'dim'
        entries = []
        #Some shortcuts...
        menu = self.info['menu']
        general = self.info['general']
        keys = self.info['menu'].keys()
        #=============================================================================
        #Creating /usr/share/applications-registry/<<package_name>> applications
        #=============================================================================
        msg = '- Preparing /usr/share/applications-registry entry...'
        c.eprint(msg, indent=1)
        path = APP_REG_ENTRY_PATH % general['package_name']
        content = general['package_name'] + "\n"
        content += "\t" + "command=" + menu['command'] + "\n"
        #Boolean properties
        boolean = (
            'can_open_multiple_files', 'expects_uris',
            'requires_terminal', 'uses_gnomevfs', 'startup_notify'
        )
        for b in boolean:
            if b in keys:
                v = str(menu[b]).lower()
                content += "\t" + b + "=" + v + "\n"
        #Optional properties
        optional = ('name', 'mime_types', 'supported_uri_schemes')
        for o in optional:
            if o in keys:
                content += "\t" + o + "=" + menu[o] + "\n"
        entries.append({'path': path, 'content': content[:-1]}) #removes last \n
        #=============================================================================
        #Creating /usr/share/menu/<<package_name>>
        #=============================================================================
        msg = '- Preparing /usr/share/menu entry...'
        c.eprint(msg, indent=1)
        path = MENU_ENTRY_PATH % general['package_name']
        content = '?package(%s): \\\n' % general['package_name']
        content += "\t" + 'command="%s"' % menu['command'] + " \\\n"
        content += "\t" + 'title="%s"' % general['name'] + " \\\n"
        content += "\t" + 'longtitle="%s"' % general['short_description'] + " \\\n"
        optional = ('needs', 'section', 'hints')
        for o in optional:
            if o in keys:
                content += "\t" + o + '="%s"' % menu[o] + " \\\n"
        if 'icon' in keys:
            content += "\t" + 'icon="/usr/share/pixmaps/%s.xpm"' % general['package_name']
        entries.append({'path': path, 'content': content})
        #=============================================================================
        # Creating /usr/share/applications/<<package_name>>.desktop (Freedesktop)
        #=============================================================================
        msg = '- Preparing /usr/share/applications entry ...'
        c.eprint(msg, indent=1)
        path = APPS_ENTRY_PATH % general['package_name']
        content = '[Desktop Entry]' + "\n"
        content += 'Type=Application' + "\n"
        content += 'Name=' + general['name'] + "\n"
        content += 'Exec=' + menu['command'] + "\n"
        content += 'Version=' + str(general['version']) + "\n"
        #Processing boolean and other fields
        for b in FREEDESKTOP_BOOLEAN.keys():
            if b in keys:
                content += FREEDESKTOP_BOOLEAN[b] + "=" + str(menu[b]).lower() + "\n"
        for o in FREEDESKTOP_OTHER.keys():
            if o in keys:
                content += FREEDESKTOP_OTHER[o] + "=" + str(menu[b]).lower() + "\n"
        #Icon
        if 'icon' in keys:
            content += "Icon=%s" % general['package_name']
        entries.append({'path': path, 'content': content})
        c.reset()
        return entries