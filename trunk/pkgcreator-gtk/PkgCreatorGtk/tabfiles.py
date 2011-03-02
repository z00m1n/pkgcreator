import subprocess
from PkgCreator.constants import DEBIAN_SECTIONS
from editabletreeview import EditableTreeView

class TabFiles:
    def __init__(self, builder, gui):
        self.builder = builder
        self.gui = gui
        vbox = self.builder.get_object("vboxFiles")
        columns = ["Source path", "Target path"]
        self.editable = EditableTreeView("Install Files", columns, gui)
        vbox.pack_start(self.editable.get_main_widget())

    def config(self):
        pass

    def from_dict(self, maindict):
        self.clear_all()
        if maindict.has_key('files'):
            for f in maindict['files']:
                self.editable.append((f['src'], f['dst']))
        return []

    def populate_dict(self, maindict):
        list = []
        model = self.editable.get_model()
        iter = model.get_iter_first()
        while iter:
            src = model.get_value(iter, 0)
            dst = model.get_value(iter, 1)
            list.append(
                {'src': src, 'dst': dst}
            )
            iter = model.iter_next(iter)
        maindict['files'] = list
    
    def validate(self):
        pass
    
    def clear_all(self):
        self.editable.get_model().clear()
    
