import subprocess
from PkgCreator.constants import DEBIAN_SECTIONS
from editabletreeview import EditableTreeView

class TabGeneral:
    def __init__(self, builder, gui):
        self.builder = builder
        self.gui = gui
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
        alignment = g("alignmentAuthors")
        self.authors = EditableTreeView("Authors", ['Name', 'Email'], gui)
        alignment.add(self.authors.get_main_widget())
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

    def from_dict(self, maindict):
        if not maindict.has_key('general'):
            return
        dict = maindict['general']
        self.clear_all()
        self.errors = []
        #Simple entries
        for widget, yamlkey in self.entryRecipes.iteritems():
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
                self.authors.append((a['name'], a['email']))
        return self.errors


    def populate_dict(self, maindict):
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
        maindict['general'] = dict
    
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
    
    def __config_architectures(self):
        #@attention: Wildcards 'all' and 'any' added in Glade
        try:
            architectures = subprocess.check_output(["dpkg-architecture", "-L"]).split()
            architectures.sort()
            #Detaching model temporarily...
            model = self.architecture.get_model()
            self.architecture.set_model(None)
            for a in architectures:
                model.append((a,))
            self.architecture.set_model(model)
        except:
            print "dpkg not installed..."

    def __config_sections(self):
        for s in DEBIAN_SECTIONS:
            self.section.get_model().append((s,))