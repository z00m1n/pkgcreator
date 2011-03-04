import subprocess
import gtk
from PkgCreator.constants import DEBIAN_SECTIONS
from entryfilechooser import EntryFileChooser

class TabMenu:
    def __init__(self, builder, gui):
        self.builder = builder
        self.gui = gui
        g = self.builder.get_object
        self.table = g("tableMenu")
        self.command = g("entryCommand")
        self.sections = g("entryMenuSections")
        self.entryfilechooser = EntryFileChooser("icon")
        self.iconfilter = g("filefilterImages")
        self.iconfilter.add_pixbuf_formats()
        self.entryfilechooser.set_filter(self.iconfilter)
        dialog = self.entryfilechooser.get_file_chooser_dialog()
        dialog.get_content_area().pack_start(gtk.Label("Image files only."))
        self.openMultipleFiles = g("checkbuttonOpenMultipleFiles")
        self.requiresTerminal = g("checkbuttonRequiresTerminal")
        self.expectsURIs = g("checkbuttonExpectsURIs")
        self.table.attach(self.entryfilechooser.get_main_widget(), 1, 2, 2, 3)

    def config(self):
        pass

    def from_dict(self, maindict):
        self.clear_all()
        if maindict.has_key('menu'):
            dict = maindict['menu']
            if dict.has_key('command'):
                self.command.set_text(dict['command'])
            if dict.has_key('section'):
                self.sections.set_text(dict['section'])
            if dict.has_key('icon'):
                self.entryfilechooser.set_value(dict['icon'])
            if dict.has_key('requires_terminal'):
                value = dict['requires_terminal']
                self.requiresTerminal.set_active(value == 'yes')
            if dict.has_key('expects_uris'):
                value = dict['expects_uris']
                self.expectsURIs.set_active(value=='yes')
            if dict.has_key('can_open_multiple_files'):
                value = dict['can_open_multiple_files']
                self.openMultipleFiles.set_active(value == 'yes')
        return []

    def populate_dict(self, maindict):
        maindict['menu'] = {}
        maindict['menu']['command'] = self.command.get_text()
        maindict['menu']['section'] = self.sections.get_text()
        maindict['menu']['icon'] = self.entryfilechooser.get_value()
        maindict['menu']['requires_terminal'] = self.requiresTerminal.get_active()
        maindict['menu']['can_open_multiple_files'] = self.openMultipleFiles.get_active()
        maindict['menu']['expects_uris'] = self.expectsURIs.get_active()
    
    def validate(self):
        pass
    
    def clear_all(self):
        self.command.set_text('')
        self.sections.set_text('')
        self.entryfilechooser.set_value('')
        self.expectsURIs.set_active(False)
        self.requiresTerminal.set_active(False)
        self.openMultipleFiles.set_active(False)
    

