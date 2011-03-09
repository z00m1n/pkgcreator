import gobject
import gtk

class EditableTreeView:
    def __init__(self, name, columns, observer=None):
        self.observer = observer
        #Treeview, columns, cells and model
        args = [gobject.TYPE_STRING] * len(columns)
        self.model = gtk.ListStore(*args)
        self.columns = []
        self.cells = []
        self.__allow_cursor_changes = False
        index = 0
        for i in columns:
            cell = gtk.CellRendererText()
            cell.set_property('editable', True)
            cell.connect("edited", self.editing_done, index)
            cell.connect("editing-started", self.__editing_started, index)
            cell.connect("editing-canceled", self.__editing_canceled)
            self.cells.append(cell)
            column = gtk.TreeViewColumn(i, cell, text = index) #map cell to model
            column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
            column.set_expand(True)
            self.columns.append(column)
            index += 1
        self.treeview = gtk.TreeView(model=self.model)
        self.treeview.set_headers_visible(True)
        self.treeview.set_reorderable(True)
        self.model.connect("row-changed", self.__row_changed)
        for c in self.columns:
            self.treeview.append_column(c)
        #Scrolled Window
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.add(self.treeview)
        #Actions
        self.action_add = gtk.Action(
             "actionAdd" + name.title(),
             "Add", "Add a new item", gtk.STOCK_ADD
        )
        self.action_remove = gtk.Action(
             "actionRemove" + name.title(),
             "Remove", "Removes selected item", gtk.STOCK_REMOVE
        )
        self.action_add.connect("activate", self.add_event)
        self.action_remove.connect("activate", self.remove_event)
        self.action_remove.set_sensitive(False)
        #Buttons Add and Remove
        self.button_add = gtk.Button(stock=gtk.STOCK_ADD)
        self.button_add.set_related_action(self.action_add)
        self.button_add.set_use_action_appearance(True)
        self.button_remove = gtk.Button(stock=gtk.STOCK_REMOVE)
        self.button_remove.set_related_action(self.action_remove)
        self.button_remove.set_use_action_appearance(True)
        #Button box
        self.hbuttonbox = gtk.HButtonBox()
        self.hbuttonbox.set_layout(gtk.BUTTONBOX_END)
        self.hbuttonbox.set_spacing(15)
        self.hbuttonbox.pack_start(self.button_add)
        self.hbuttonbox.pack_start(self.button_remove)
        #Vertical Box
        self.vbox = gtk.VBox()
        self.vbox.pack_start(self.scrolled_window)
        self.vbox.pack_start(self.hbuttonbox)
        self.vbox.set_child_packing(
            self.hbuttonbox, expand=False, fill=True,
            padding = 0, pack_type=gtk.PACK_START)

    def get_main_widget(self):
        return self.vbox

    def get_model(self):
        return self.model

    def add_event(self, widget):
        self.model.append()
        elements = self.length()
        self.treeview.set_cursor_on_cell(
            elements - 1, 
            focus_column = self.columns[0],
            focus_cell= self.cells[0],
            start_editing=True)
        self.action_remove.set_sensitive(True)
        return True

    def remove_event(self, widget):
        rows = self.treeview.get_selection().get_selected_rows()[1]
        for r in rows:
            iter = self.model.get_iter(r)
            self.model.remove(iter)
        if self.model.get_iter_first() == '0':
            self.action_remove.set_sensitive(False)

    def editing_done(self, widget, path, text, index):
        iter = self.model.get_iter(path)
        self.model.set_value(iter, index, text)
        if self.observer:
            self.observer.data_changed(self)
        return True
    
    def append(self, row):
        self.model.append(row)
        self.action_remove.set_sensitive(True)
    
    def length(self):
        return self.model.iter_n_children(None)

    def __editing_started(self, cell, celleditable, path, num_col):
        celleditable.connect("key-press-event", self.__keypressed_editablecell, 
                             cell, path, num_col)
        return True
    
    def __editing_canceled(self, cell):
        path_last = self.length() - 1
        iter = self.model.get_iter(path_last)
        self.__row_changed(None, path_last, iter)
    
    def __row_changed(self, model, path, iter):
        #Checking if the last line is empty
        for index in range(len(self.columns)):
            if self.model.get_value(iter, index) not in [None, '']:
                return False
        if self.__line_is_blank(path):
            self.model.remove(iter)
        if self.length() == 0:
            self.action_remove.set_sensitive(False)
        return False

    def __line_is_blank(self, path):
        iter = self.model.get_iter(path)
        for index in range(len(self.columns)):
            if self.model.get_value(iter, index) not in [None, '']:
                return False
        return True

    def __keypressed_editablecell(self, widget, event, cell, path, num_col):
        if (event.keyval == gtk.keysyms.Tab):
            return self.__tabpressed(cell, path, widget.get_text(), num_col)
        else:
            return False

    def __tabpressed(self, cell, path, new_text, num_col):
         self.editing_done(cell, path, new_text, num_col)
         num_col += 1
         if (num_col < len(self.columns)):
             viewcolumn = self.treeview.get_column(num_col)
             self.treeview.set_cursor(path, viewcolumn, True)
         else:
             self.add_event(None)
         return False

if __name__ == "__main__":
    win = gtk.Window()
    tree = EditableTreeView("teste", ['Name', 'Phone'])
    win.add(tree.get_main_widget())
    win.show_all()
    win.connect("destroy", gtk.main_quit)
    gtk.main()
