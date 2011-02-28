import subprocess
import gtk
import resources
from documentform import DocumentForm
from PkgCreator.constants import DEBIAN_SECTIONS


class GUI:
    def __init__(self):
        #Builder and main window
        self.builder = gtk.Builder()
        self.builder.add_from_file(resources.GUI_PATH)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.window.connect("destroy", gtk.main_quit)
        #Dialogs
        self.about = self.builder.get_object("aboutdialog1")
        self.msgdiagSaveChanges = self.builder.get_object("msgdiagSaveChanges")
        self.msgdiagErrorFile = self.builder.get_object("msgdiagErrorFile")
        #File dialogs related
        self.fileDiagOpen = self.builder.get_object("filechooserOpen")
        self.fileDiagSave = self.builder.get_object("filechooserSave")
        self.buttonDiagSave = self.builder.get_object("buttonDiagSave")
        self.buttonDiagOpen = self.builder.get_object("buttonDiagOpen")
        #Combo boxes and list stores
        self.listStoreArchitectures = self.builder.get_object("liststoreArchitectures")
        self.comboBoxArchitectures = self.builder.get_object("comboboxArchitectures")
        self.listStoreSection = self.builder.get_object("liststoreSections")
        #Other properties
        self.filename = None
        self.documentForm = DocumentForm(self.builder)
        #Config procedure
        self.__config_file_choosing()
        self.__config_architectures()
        self.__config_sections()
        self.__config_actions()

    def show(self):
        self.window.show_all()
        gtk.main()

    def quit(self, widget, *event):
        if(self.__warn_user()):
            gtk.main_quit()

    def show_about(self, widget, *event):
        self.about.run()
        self.about.hide()

    def new(self, widget, *event):
        if(self.__warn_user()):
            print "Create new file..."

    def open(self, widget, *event):
        if(self.__warn_user()):
            response = self.fileDiagOpen.run()
            self.fileDiagOpen.hide()
            if response == 2:
                filename = self.fileDiagOpen.get_filename()
                if filename and filename.endswith(".yaml"):
                    self.documentform.load(filename)
                    self.actionsPrjOpened.set_sensitive(True)
                else:
                    self.msgdiagErrorFile.run()
                    self.msgdiagErrorFile.hide()

    def save(self, widget=None, *event):
        if self.filename:
            #Save me!
            pass
        else:
            self.save_as()

    def save_as(self, widget=None, *event):
        response = self.fileDiagSave.run()
        self.fileDiagSave.hide()
        if response == 2:
            filename = self.fileDiagSave.get_filename()
            if filename and filename.endswith(".yaml"):
                self.filename = filename
                self.documentform.save(filename)
                self.actionsSave.set_sensitive(False)
            else:
                self.msgdiagErrorFile.run()
                self.msgdiagErrorFile.hide()

    def undo(self, widget, *event):
        print "Undo"

    def redo(self, widget, *event):
        print "Redo"

    def data_changed(self, widget, *event):
        print "Data changed!"
        self.actionsSave.set_sensitive(True)

    def add_author(self, widget, *event):
        print "Add author"
        self.actionsSave.set_sensitive(True)

    def remove_author(self, widget, *event):
        print "Remove author"
        self.actionsSave.set_sensitive(True)

    def run_pkgcreator(self, widget, *event):
        print "Run pkgcreator"
        """if file exists, save it and run
        else, warn user that he must save the file before creating the pkg"""

    def __warn_user(self):
        if self.actionsSave.get_sensitive():    #or if document.has_changes()
            response = self.msgdiagSaveChanges.run()
            self.msgdiagSaveChanges.hide()
            if response == 1: return True       #proceed without saving
            elif response == 2: return False    #cancel operation
            elif response == 3:                 #save and proceed
                self.save()
                return True
        else:                                   #proceed
            return True

    def __config_file_choosing(self):
        filefilter = self.builder.get_object("filefilterYAML")
        filefilter.add_mime_type('application/x-yaml')

    def __config_architectures(self):
        #@attention: Wildcards 'all' and 'any' added in Glade
        architectures = subprocess.check_output(["dpkg-architecture", "-L"]).split()
        architectures.sort()
        for a in architectures:
            self.listStoreArchitectures.append((a,))

    def __config_sections(self):
        for s in DEBIAN_SECTIONS:
            self.listStoreSections.append((s,))

    def __config_actions(self):
        self.actionsSave = gtk.ActionGroup("SaveCommands")
        self.actionsSave.add_action(self.builder.get_object("actionSave"))
        self.actionsSave.add_action(self.builder.get_object("actionSaveAs"))
        self.actionsSave.set_sensitive(False)
        #With a project opened: Run pkgcreator, validate document, run lintian, etc...
        self.actionsPrjOpened = gtk.ActionGroup("ProjectOpened")
        self.actionsPrjOpened.add_action(self.builder.get_object("actionRunPkgCreator"))
        self.actionsPrjOpened.set_sensitive(False)