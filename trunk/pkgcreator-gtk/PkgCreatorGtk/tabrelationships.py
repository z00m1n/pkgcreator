import subprocess
from PkgCreator.constants import DEBIAN_SECTIONS
from editabletreeview import EditableTreeView

class TabRelationships:
    def __init__(self, builder, gui):
        self.builder = builder
        self.gui = gui
        g = self.builder.get_object
        columns = ['Name', 'Version']
        self.__maskedvars = {}
        self.regions = ['Depends', 'Recommends', 'Suggests', 'PreDepends']
        for r in self.regions:
            self[r.lower()] = EditableTreeView(r, columns, gui)
            g("alignment" + r).add(self[r.lower()].get_main_widget())

    def config(self):
        pass

    def from_dict(self, dict):
        self.clear_all()
        for r in self.regions:
            if dict.has_key(r.lower()):
                for f in dict[r.lower()]:
                    assert f.has_key('name')
                    if not f.has_key('version'):
                        f['version'] = ''
                    self[r.lower()].append((f['name'], f['version']))
        return []

    def populate_dict(self, maindict):
        dict = {}
        for r in self.regions:
            maindict[r.lower()] = []
            model = self[r.lower()].get_model()
            iter = model.get_iter_first()
            while iter:
                maindict[r.lower()].append(
                    {'name': model.get_value(iter, 0), 'version': model.get_value(iter, 1)}
                )
                iter = model.iter_next(iter)
    
    def validate(self):
        pass
    
    def clear_all(self):
        for r in self.regions:
            self[r.lower()].get_model().clear()
    
    def __setitem__(self, key, value):
        self.__maskedvars[key] = value
    
    def __getitem__(self, key):
        return self.__maskedvars[key]
