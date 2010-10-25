import yaml

class Validator:
    def create_from_string(string):
        self.markup = string
    def create_from_file(path):
        with open(path) as f:
            self.markup = f.read()
