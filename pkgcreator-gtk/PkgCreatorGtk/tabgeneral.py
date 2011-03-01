import subprocess
from PkgCreator.constants import DEBIAN_SECTIONS

class TabGeneral:
    def __init__(self, builder):
        self.builder = builder
        g = self.builder.get_object
        #Widgets related to the "general" section
        self.pkgname = g("entryPkgName")
        self.prjname = g("entryPrjName")
        self.version = g("entryVersion")
        self.homepage = g("entryHomepage")
        self.shortdesc = g("entryShortDescription")
        self.maintname = g("entryMaintainerName")
        self.maintemail = g("entryMaintainerEmail")
        self.longdesc = g("textviewLongDescription")
        self.architecture = g("comboboxArchitectures")
        self.priority = g("comboboxPriorities")
        self.section = g("comboboxSections")
        self.essential = g("comboboxEssential")
        #Authors
        self.authors = g("treeviewAuthors")
        self.cellauthorname = g("cellauthorname")
        self.cellauthoremail = g("cellauthoremail")
        self.columnauthorname = g("tvcolumnAuthorName")
        self.actionremove = g("actionRemoveAuthor")
        #Recipes
        self.entryRecipes = {
            self.pkgname: 'package_name',
            self.prjname: 'name',
            self.version: 'version', 
            self.homepage: 'homepage',
            self.shortdesc: 'short_description',
        }
        self.comboRecipes = {
            self.architecture: 'architecture',
            self.priority: 'priority',
            self.section: 'section',
            self.essential: 'essential'
        }

    def config(self):
        self.__config_architectures()
        self.__config_sections()

    def from_dict(self, dict):
        self.errors = []
        #Simple entries
        for widget, yamlkey in self.entryRecipes.iteritems():
            print yamlkey
            if yamlkey in dict.keys():
                widget.set_text(str(dict[yamlkey]))
        #Maintainer entries
        #@todo: automatic mapping
        #maintainer/email/foo ==> dict['maintainer']['email']['foo']
        if dict.has_key('maintainer'):
            if dict['maintainer'].has_key('name'):
                self.maintname.set_text(dict['maintainer']['name'])
            if dict['maintainer'].has_key('email'):
                self.maintemail.set_text(dict['maintainer']['email'])
        #Combo boxes
        for widget, yamlkey in self.comboRecipes.iteritems():
            if yamlkey in dict.keys():
                value = dict[yamlkey]
                model = widget.get_model()
                iter = model.get_iter_first()
                while iter:
                    if model.get(iter, 0)[0] == value:
                        widget.set_active_iter(iter)
                        break
                    else:
                        iter = model.iter_next(iter)
                if not iter:
                    print "ERROR! Item did not match any possible choice..."
                    self.errors.append(widget)
        #Long description
        if dict.has_key('long_description'):
            self.longdesc.get_buffer().set_text(dict['long_description'])
        #Authors
        if dict.has_key('authors'):
            for a in dict['authors']:
                self.authors.get_model().append((a['name'], a['email']))
        return self.errors


    def to_dict(self):
        dict = {}
        #Entries
        for widget, yamlkey in self.entryRecipes.iteritems():
            dict[yamlkey] = widget.get_text()
        #Textviews
        ldbuf = self.longdesc.get_buffer()
        iters = ldbuf.get_bounds()
        dict['long_description'] = ldbuf.get_text(iters[0], iters[1])
        #Maintainer entries
        dict['maintainer'] = {}
        dict['maintainer']['name'] = self.maintname.get_text()
        dict['maintainer']['email'] = self.maintemail.get_text()
        #Combo boxes
        for widget, yamlkey in self.comboRecipes.iteritems():
            model = widget.get_model()
            iter = widget.get_active_iter()
            value = model.get(iter, 0)[0]
            if value != '(not specified)':
                dict[yamlkey] = value
        #Authors
        dict['authors'] = []
        iter = self.authors.get_model().get_iter_first()
        while iter:
            name = self.authors.get_model().get_value(iter, 0)
            email = self.authors.get_model().get_value(iter, 1)
            dict['authors'].append(
                {'name': name, 'email': email}
            )
            iter = self.authors.get_model().iter_next(iter)
        return dict
    
    def validate(self):
        pass
    
    def clear_all(self):
        #Entries
        for e in self.entryRecipes.keys():
            e.set_text('')
        self.maintname.set_text('')
        self.maintemail.set_text('')
        #Textviews
        self.longdesc.get_buffer().set_text('')
        #Combos
        for c in self.comboRecipes.keys():
            c.set_active(0)
        #Authors
        self.authors.get_model().clear()
    
    def add_author(self):
        self.authors.get_model().append()
        elements = self.authors.get_model().iter_n_children(None)
        self.authors.set_cursor_on_cell(
            elements - 1, 
            focus_column = self.columnauthorname,
            focus_cell= self.cellauthorname,
            start_editing=True)
        self.actionremove.set_sensitive(True)
    
    def remove_author(self):
        rows = self.authors.get_selection().get_selected_rows()[1]
        for r in rows:
            iter = self.authors.get_model().get_iter(r)
            self.authors.get_model().remove(iter)
        if self.authors.get_model().get_iter_first() == '0':
            self.actionremove.set_sensitive(False)

    def author_changed(self, widget, path, text):
        iter = self.authors.get_model().get_iter(path)
        if widget == self.cellauthorname:
            self.authors.get_model().set_value(iter, 0, text)
        elif widget == self.cellauthoremail:
            self.authors.get_model().set_value(iter, 1, text)
    
    def __config_architectures(self):
        #@attention: Wildcards 'all' and 'any' added in Glade
        try:
            architectures = subprocess.check_output(["dpkg-architecture", "-L"]).split()
            architectures.sort()
            for a in architectures:
                self.architecture.get_model().append((a,))
        except:
            print "dpkg not installed..."

    def __config_sections(self):
        for s in DEBIAN_SECTIONS:
            self.section.get_model().append((s,))
