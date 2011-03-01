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
        #Recipes
        self.entryRecipes = {
            self.pkgname: 'package_name',
            self.prjname: 'name',
            self.version: 'version', 
            self.homepage: 'homepage',
            self.shortdesc: 'short_description'
        }
        self.comboRecipes = {
            self.architecture: 'architecture',
            self.priority: 'priority',
            self.section: 'section',
            self.essential: 'essential'
        }

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
        return self.errors

    def to_dict(self):
        self.dict = {}
        #Entries
        for widget, yamlkey in self.entryRecipes.iteritems():
            self.dict[yamlkey] = widget.get_text()
        #Maintainer entries
        self.dict['maintainer'] = {}
        self.dict['maintainer']['name'] = self.maintname.get_text()
        self.dict['maintainer']['email'] = self.maintemail.get_text()
        #Combo boxes
        for widget, yamlkey in self.comboRecipes.iteritems():
            model = widget.get_model()
            iter = widget.get_active_iter()
            value = model.get(iter, 0)[0]
            if value != '(not specified)':
                self.dict[yamlkey] = value
        return self.dict
    
    def validate(self):
        pass
