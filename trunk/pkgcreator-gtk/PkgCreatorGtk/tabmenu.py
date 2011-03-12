import os
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
        self.openMultipleFiles = g("checkbuttonOpenMultipleFiles")
        self.requiresTerminal = g("checkbuttonRequiresTerminal")
        self.expectsURIs = g("checkbuttonExpectsURIs")
        #Icon choosing
        label = gtk.Label("Image files (*.png, *.jpg, *.gif, ...)")
        self.preview = gtk.Image()
        self.entryfilechooser = EntryFileChooser("icon", [self])
        icon_diag = self.entryfilechooser.get_file_chooser_dialog()
        icon_diag.set_preview_widget(self.preview)
        icon_diag.set_extra_widget(label)
        icon_diag.connect('update-preview', self.__icon_preview, self.preview) 
        self.iconfilter = g("filefilterImages")
        self.iconfilter.add_pixbuf_formats()
        self.entryfilechooser.set_filter(self.iconfilter)
        self.image = g('imageIcon')
        dialog = self.entryfilechooser.get_file_chooser_dialog()
        dialog.get_content_area().pack_start(gtk.Label("Image files only."))
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
        maindict['menu']['needs'] = 'X11' #@todo: add this option in GUI
    
    def validate(self):
        pass
    
    def clear_all(self):
        self.command.set_text('')
        self.sections.set_text('')
        self.entryfilechooser.set_value('')
        self.expectsURIs.set_active(False)
        self.requiresTerminal.set_active(False)
        self.openMultipleFiles.set_active(False)
    
    def __icon_preview(self, file_chooser, preview):
        filename = file_chooser.get_preview_filename()
        try:
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, 128, 128)
            preview.set_from_pixbuf(pixbuf)
            have_preview = True
        except:
            have_preview = False
        file_chooser.set_preview_widget_active(have_preview)
        return
    
    def data_changed(self, who):
        missing_icon = lambda: self.image.set_from_icon_name('gtk-missing', 
                                                             gtk.ICON_SIZE_LARGE_TOOLBAR)
        if who == self.entryfilechooser:
            text = self.entryfilechooser.get_entry().get_text()
            if os.path.isabs(text):
                filename = text
            else:
                filename = None
                base_path = self.gui.get_base_path()
                if base_path:
                    filename = os.path.join(base_path, text)
                    if not os.path.exists(filename):
                        filename = None
            #Setting new image
            if filename is None:
                missing_icon()
            else:
                try:
                    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, 128, 128)
                    self.image.set_from_pixbuf(pixbuf)
                except:
                    missing_icon()

