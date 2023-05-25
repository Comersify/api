import os


class MakeEnvVariables:
    def __init__(self, path='.env'):
        self.env_file = open(path,'r').read().split('\n')
        self.variables = {}
        self.default_keys = ['ENV', 'SECRET_NAME']
        self.is_on_dev = None

    def read_env_file(self):
        for var in self.env_file:
            splitted_var = var.replace("'","").split('=') 
            if splitted_var != ['']:
                if len(splitted_var) > 2 :
                    splitted_var = [splitted_var[0], ''.join(splitted_var[1:])]
                self.variables[splitted_var[0]] = splitted_var[1]

    def read_keys(self):
        self.keys = self.variables.keys()

    def is_runing_on_dev(self):
        return self.variables['ENV'] == 'DEV' 

    def set_env_variables(self):
        for key in self.keys:
            if self.is_on_dev and (key in self.default_keys): 
                os.environ[key] = self.variables[key]
            else:
                os.environ[key] = self.variables[key]

    def run(self):
        print("Setting ENV variables ...")
        self.read_env_file()
        self.read_keys()
        self.is_runing_on_dev()
        self.set_env_variables()

        