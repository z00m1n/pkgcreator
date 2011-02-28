'''Data Structure used:
    Dicts of dicts
     1st level dict key => user input widget names
     2st level dict keys:
         - widget
         - obrigatory
         - validate_function
         - load_function
         - save_function
'''


USER_INPUTS = (
    'entryPkgName', 'entryPrjName', 'entryVersion', 'entryHomePage',
    'entryMaintainerName', 'entryMaintainerEmail', 'entryShortDescription',
    'textviewLongDescription', 'comboboxArchitectures',
    'comboboxPriority', 'comboboxSections', 'comboboxEssential'
)

class DocumentForm:
    def __init__(self, builder):
        self.builder = builder
        #General Tab
        self.user_inputs = {}
        for w in USER_INPUTS:
            self.user_inputs[w] = self.builder.get_object(w)

    def load(self, path):
        '''Loads a pkgcreator's YAML file and fill the form with its contents.'''
        pass

    def save(self, path):
        '''Saves the form data into a pkgcreator's YAML file'''
        for name, widget in self.user_inputs.iteritems():
            if name.beginswith('entry') or name.beginswith('textview'):
                value = widget.get_text()
            elif name.beginswith('combobox'):
                value =
        pass

    def validate(self):
        '''Validate all fields.

        Returns a list of invalid fields or an empty list if all fields are valid.
        '''
        #@note: Parse kwalify output to get invalid or absent fields!
        pass
    
