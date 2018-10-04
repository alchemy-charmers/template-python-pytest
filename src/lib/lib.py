from charmhelpers.core import hookenv, host
from charms import layer


class ${libclass}():
    def __init__(self):
        self.charm_config = hookenv.config()

    def action_function(self):
        ''' An example function for calling from an action '''
        return
