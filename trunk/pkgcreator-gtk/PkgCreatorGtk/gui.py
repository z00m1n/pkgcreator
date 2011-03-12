import sys
import os
import subprocess
import yaml
import glib
import gobject
import gtk
import vte
import copy
import resources
from tabgeneral import TabGeneral
from tabfiles import TabFiles
from tabrelationships import TabRelationships
from tabmenu import TabMenu

PKGCREATOR_MSG = 'In order to create proper Debian packages root privileges ' \
                 'are needed.'
CONFIRM_MSG1 = 'Save changes to project %s before proceeding?'
CONFIRM_MSG2 = 'Save changes before proceeding?'

class GUI:
    def __init__(self):
        #Builder and main window
        glib.set_application_name("pkgcreator-gtk")
        self.filename = None
        self.dict = {}
        self.phase = 0

    def start(self, splash=False):
        if splash:
            self.splash_window = gtk.Window()
            self.splash_window.set_default_size(200,200)
            self.splash_window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
            self.splash_window.set_decorated(False)
            self.splash_window.set_skip_taskbar_hint(True)
            self.splash_window.set_skip_pager_hint(True)
            self.splash_window.set_urgency_hint(True)
            self.splash_window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_SPLASHSCREEN)
            
            vbox = gtk.VBox(spacing=5)
            label = gtk.Label('<b>Loading pkgcreator-gtk...</b>')
            label.set_use_markup(True)
            self.splash_label = gtk.Label('Building GUI...')
            spinner = gtk.Spinner()
            spinner.start()
            vbox.pack_start(label, False)
            vbox.pack_start(self.splash_label, False)
            vbox.pack_start(spinner, True)
            self.splash_window.add(vbox)
            self.splash_window.show_all()
            while gtk.events_pending():
                gtk.main_iteration()
            gobject.idle_add(self.__init_gradually)
        else:
            #Make all GUI preparation at once
            self.__init_builder()
            self.__init_tabs_handlers()
            self.__init_widgets()
            self.__init_vte()
            self.__config()
            self.__show()
        gtk.main()

    def quit(self, widget=None, *event):
        if(self.__warn_user()):
            gtk.main_quit()

    def show_about(self, widget, *event):
        self.about.run()
        self.about.hide()

    #Initialization related

    def __init_gradually(self):
        if self.phase == 0:
            self.__init_builder()
            self.splash_label.set_text('Getting context handlers...')
        elif self.phase == 1:
            self.__init_tabs_handlers()
            self.splash_label.set_text('Getting widgets...')
        elif self.phase == 2:
            self.__init_widgets()
            self.splash_label.set_text('Initializing virtual terminal...')
        elif self.phase == 3:
            self.__init_vte()
            self.splash_label.set_text('Configuring main widgets...')
        elif self.phase == 4:
            self.__config()
        elif self.phase > 4:
            self.splash_window.hide()
            self.__show()
            return False
        sys.stdout.flush()
        self.phase += 1
        return True

    def __init_builder(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(resources.GUI_PATH)

    def __init_tabs_handlers(self):
        self.tabgeneral = TabGeneral(self.builder, self)
        self.tabrelationships = TabRelationships(self.builder, self)
        self.tabfiles = TabFiles(self.builder, self)
        self.tabmenu = TabMenu(self.builder, self)
    
    def __init_widgets(self):
        self.window = self.builder.get_object("window1")
        self.about = self.builder.get_object("aboutdialog1")
        self.diagRunning = self.builder.get_object("dialogRunning")
        self.msgdiagSaveChanges = self.builder.get_object("msgdiagSaveChanges")
        self.msgdiagErrorFile = self.builder.get_object("msgdiagErrorFile")
        self.fileDiagOpen = self.builder.get_object("filechooserOpen")
        self.fileDiagSave = self.builder.get_object("filechooserSave")
        self.buttonDiagSave = self.builder.get_object("buttonDiagSave")
        self.buttonDiagOpen = self.builder.get_object("buttonDiagOpen")
        self.buttonRunningDiagClose = self.builder.get_object("buttonRunningDiagClose")
    
    def __init_vte(self):
        self.terminal = vte.Terminal()
        self.terminal.connect("child-exited", self.pkgcreator_ended)
        self.terminal.show()
        self.diagRunning.get_content_area().pack_start(self.terminal)

    def __config(self):
        self.__config_file_choosing()
        self.tabgeneral.config()
        self.__config_actions()
        self.__update_title()
        self.tabgeneral.clear_all()
        self.builder.connect_signals(self)
        self.window.connect("destroy", self.quit)

    def __show(self):
        self.window.show_all()

    #File related

    def new(self, widget, *event):
        if(self.__warn_user()):
            self.filename = None
            self.__update_title()
            self.dict = {}
            self.tabgeneral.clear_all()
            self.tabfiles.clear_all()
            self.tabrelationships.clear_all()
            self.tabmenu.clear_all()
            self.actionSave.set_sensitive(False)
            self.actionSaveAs.set_sensitive(False)
            self.actionRunPkgCreator.set_sensitive(False)
            #clear output

    def open(self, widget, *event):
        if(self.__warn_user()):
            response = self.fileDiagOpen.run()
            self.fileDiagOpen.hide()
            if response == gtk.RESPONSE_OK:
                filename = self.fileDiagOpen.get_filename()
                self.load_file(filename)
            else:
                self.msgdiagErrorFile.run()
                self.msgdiagErrorFile.hide()

    def save(self, widget=None, *event):
        if self.filename:
            self.dict = {}
            self.tabgeneral.populate_dict(self.dict)
            self.tabfiles.populate_dict(self.dict)
            self.tabrelationships.populate_dict(self.dict)
            self.tabmenu.populate_dict(self.dict)
            self.dict = self.__remove_blank_entries(self.dict)
            with open(self.filename, 'w') as f:
                yaml.dump(self.dict, f)
            self.actionSave.set_sensitive(False)
        else:
            self.save_as()

    def save_as(self, widget=None, *event):
        response = self.fileDiagSave.run()
        self.fileDiagSave.hide()
        if response == gtk.RESPONSE_OK:
            filename = self.fileDiagSave.get_filename()
            if filename and filename.endswith(".yaml"):
                self.filename = filename
                self.save()
                self.__update_title()
            else:
                self.msgdiagErrorFile.run()
                self.msgdiagErrorFile.hide()

    def data_changed(self, widget, *event):
        self.actionSave.set_sensitive(True)
        self.actionSaveAs.set_sensitive(True)
        self.__update_title(False)
        
    def expander_activated(self, widget, *event):
        self.tabrelationships.expander_activated(widget)

    #History related

    def undo(self, widget, *event):
        print "Undo"

    def redo(self, widget, *event):
        print "Redo"

    #PkgCreator, kwalify and lintian related
    
    def run_pkgcreator(self, widget, *event):
        self.terminal.reset(True, True)
        self.buttonRunningDiagClose.set_sensitive(False)
        self.terminal.fork_command()
        args = (PKGCREATOR_MSG, self.filename)
        cmd = "gksu -m '%s' 'pkgcreator -c %s';exit\n" % args
        self.terminal.feed_child(cmd) 
        self.diagRunning.run()
        self.diagRunning.hide()
        
    def pkgcreator_ended(self, widget, *event):
        self.buttonRunningDiagClose.set_sensitive(True)

    #Services for cmd

    def load_file(self, filename):
        if filename and filename.endswith(".yaml"):
            with open(filename) as f:
                try:
                    self.dict = yaml.load(f)
                    self.tabgeneral.from_dict(self.dict)
                    self.tabfiles.from_dict(self.dict)
                    self.tabrelationships.from_dict(self.dict)
                    self.tabmenu.from_dict(self.dict)
                    self.actionSave.set_sensitive(False)
                    self.actionRunPkgCreator.set_sensitive(True)
                    self.actionSaveAs.set_sensitive(True)
                    self.filename = filename
                except Exception as e:
                    #@todo: Put a msg box here
                    print "INVALID FILE!"
                    print e
                finally:
                    self.__update_title()
        else:
            #@todo: Put a msg box here
            print "Invalid file..."

    #Private methods
    

    def __remove_blank_entries(self, mixed):
        #Recursive method for removing blank entries
        #High memory consumption
        newmixed = copy.copy(mixed)
        if type(newmixed) == dict:
            items = mixed.keys()
        elif type(newmixed) == list:
            items = range(len(newmixed))
        for i in items:
            if not newmixed[i]:
                del newmixed[i]
            elif type(newmixed[i]) in [dict, list]:
                newmixed[i] = self.__remove_blank_entries(newmixed[i])
        return newmixed

    def __update_title(self, saved=True):
        title = 'pkgcreator-gtk :: '
        if not saved:
            title += '* '
        if self.filename:
            self.window.set_title(title + os.path.basename(self.filename))
        else:
            self.window.set_title(title + '<untitled project>')
    
    def __warn_user(self):
        if self.filename:
            self.msgdiagSaveChanges.set_markup(CONFIRM_MSG1 % os.path.basename(self.filename))
        else:
            self.msgdiagSaveChanges.set_markup(CONFIRM_MSG2)
        if self.actionSave.get_sensitive():                     #or if document.has_changes()
            response = self.msgdiagSaveChanges.run()
            self.msgdiagSaveChanges.hide()
            if response == gtk.RESPONSE_NO: return True         #proceed without saving
            elif response == gtk.RESPONSE_CANCEL: return False  #cancel operation
            elif response == gtk.RESPONSE_YES:                  #save and proceed
                self.save()
                return True
        else:                                   #proceed
            return True

    def __config_file_choosing(self):
        filefilter = self.builder.get_object("filefilterYAML")
        filefilter.add_mime_type('application/x-yaml')

    def __config_actions(self):
        self.actionSave = self.builder.get_object("actionSave")
        self.actionSaveAs = self.builder.get_object("actionSaveAs")
        self.actionRunPkgCreator = self.builder.get_object("actionRunPkgCreator")
        self.actionSave.set_sensitive(False)
        self.actionSaveAs.set_sensitive(False)
        self.actionRunPkgCreator.set_sensitive(False)
