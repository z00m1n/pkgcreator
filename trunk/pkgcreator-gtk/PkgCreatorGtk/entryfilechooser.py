import os
import gtk

class EntryFileChooser:
    def __init__(self, name, observer=None):
        self.observer = observer
        self.entry = gtk.Entry()
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
        self.hbox.pack_start(self.entry)
        self.hbox.pack_start(self.chooseButton)
        self.hbox.set_child_packing(
            self.chooseButton, expand=False, fill=True,
            padding=0, pack_type=gtk.PACK_START
        )
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

    def get_value(self):
        return self.entry.get_text()

    def set_value(self, text):
        self.entry.set_text(text)
        if os.path.isabs(text) and os.path.exists(text):
            self.dialog.set_filename(text)
        if self.observer:
            self.observer.data_changed(self)

    def set_filter(self, filter):
        self.dialog.set_filter(filter)

    def run_file_chooser(self, widget, *event):
        response = self.dialog.run()
        if response == gtk.RESPONSE_OK:
            self.entry.set_text(self.dialog.get_filename())
            self.observer.data_changed()
        self.dialog.hide()
        
if __name__ == "__main__":
    win = gtk.Window()
    widget = EntryFileChooser("teste")
    win.add(widget.get_main_widget())
    win.show_all()
    gtk.main()