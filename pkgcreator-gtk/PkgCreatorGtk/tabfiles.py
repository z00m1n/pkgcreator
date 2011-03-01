import subprocess
from PkgCreator.constants import DEBIAN_SECTIONS

class TabFiles:
    def __init__(self, builder):
        self.builder = builder
        g = self.builder.get_object
        self.tree = g("treeviewFiles")
        self.model = self.tree.get_model()
        self.cellsourcepath = g("cellsourcepath")
        self.celltargetpath = g("celltargetpath")
        self.columnsourcepath = g("tvcolumnSource")
        self.actionremove = g("actionRemoveInstallFile")

    def config(self):
        pass

    def from_list(self, list):
        self.clear_all()
        if list:
            for f in list:
                self.model.append((f['src'], f['dst']))
            self.actionremove.set_sensitive(True)
        return []

    def to_list(self):
        list = []
        iter = self.model.get_iter_first()
        while iter:
            src = self.model.get_value(iter, 0)
            dst = self.model.get_value(iter, 1)
            list.append(
                {'src': src, 'dst': dst}
            )
            iter = self.model.iter_next(iter)
        return list
    
    def validate(self):
        pass
    
    def clear_all(self):
        self.model.clear()
    
    def add_install_file(self):
        self.model.append()
        elements = self.model.iter_n_children(None)
        self.tree.set_cursor_on_cell(
            elements - 1, 
            focus_column = self.columnsourcepath,
            focus_cell= self.cellsourcepath,
            start_editing=True)
        self.actionremove.set_sensitive(True)
    
    def remove_install_file(self):
        rows = self.tree.get_selection().get_selected_rows()[1]
        for r in rows:
            iter = self.model.get_iter(r)
            self.model.remove(iter)
        if self.model.get_iter_first() == '0':
            self.actionremove.set_sensitive(False)

    def install_file_edited(self, widget, path, text):
        iter = self.model.get_iter(path)
        if widget == self.cellsourcepath:
            self.model.set_value(iter, 0, text)
        elif widget == self.celltargetpath:
            self.model.set_value(iter, 1, text)
        else:
            print text
    
