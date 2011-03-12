import os
import gtk

class EntryFileChooser:
    def __init__(self, name, observers=[]):
        self.observers = observers
        self.entry = gtk.Entry()
        self.entry.connect("changed", self.__notify_observers)
        #Button
        self.action = gtk.Action(
             "actionChooseFile" + name.title(), 
             "Choose", "Choose a file", gtk.STOCK_OPEN
        )
        self.action.connect("activate", self.run_file_chooser)
        self.chooseButton = gtk.Button(stock=gtk.STOCK_OPEN)
        self.chooseButton.set_related_action(self.action)
        self.chooseButton.set_use_action_appearance(True)
        #HBox
        self.hbox = gtk.HBox()
        self.hbox.pack_start(self.entry, True, True)
        self.hbox.pack_start(self.chooseButton, False, True)
        #File chooser dialog
        self.dialog = gtk.FileChooserDialog(
            title = "Choose a file...",
            action = gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                       gtk.STOCK_OK, gtk.RESPONSE_OK)
        )

    def get_main_widget(self):
        return self.hbox
    
    def get_file_chooser_dialog(self):
        return self.dialog
    
    def get_entry(self):
        return self.entry

    def get_value(self):
        return self.entry.get_text()

    def set_value(self, text):
        self.entry.set_text(text)
        if os.path.isabs(text) and os.path.exists(text):
            self.dialog.set_filename(text)
        self.__notify_observers()

    def set_filter(self, filter):
        self.dialog.set_filter(filter)

    def run_file_chooser(self, widget, *event):
        response = self.dialog.run()
        if response == gtk.RESPONSE_OK:
            self.entry.set_text(self.dialog.get_filename())
        self.dialog.hide()
        self.__notify_observers()
    
    def __notify_observers(self, widget=None):
        for i in self.observers:
            i.data_changed(self)
        
        
if __name__ == "__main__":
    win = gtk.Window()
    widget = EntryFileChooser("teste")
    win.add(widget.get_main_widget())
    win.show_all()
    gtk.main()