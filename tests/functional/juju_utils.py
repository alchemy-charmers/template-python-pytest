import json
import juju

from juju.errors import JujuError


class JujuUtils:
    def __init__(self, controller, model):
        self.controller = controller
        self.model = model

    async def get_app(self, name):
        '''Returns the application requested'''
        app = None
        try:
            app = self.model.applications[name]
        except KeyError:
            raise JujuError("Cannot find application {}".format(name))
        return app

    async def get_unit(self, name):
        '''Returns the requested <app_name>/<unit_number> unit'''
        unit = None
        try:
            (app_name, unit_number) = name.split('/')
            unit = self.model.applications[app_name].units[unit_number]
        except (KeyError, ValueError):
            raise JujuError("Cannot find unit {}".format(name))
        return unit

    async def get_entity(self, name):
        '''Returns a unit or an application'''
        entity = None
        try:
            entity = await self.get_unit(name)
        except JujuError:
            try:
                entity = await self.get_app(name)
            except JujuError:
                raise JujuError("Cannot find entity {}".format(name))
        return entity

    async def run_command(self, cmd, target):
        '''
        Runs a command on a unit.

        :param cmd: Command to be run
        :param target: Unit object or unit name string
        '''
        unit = (
            target
            if isinstance(target, juju.unit.Unit)
            else await self.get_unit(target)
        )
        action = await unit.run(cmd)
        return action.results

    async def file_stat(self, path, target):
        '''
        Runs stat on a file

        :param path: File path
        :param target: Unit object or unit name string
        '''
        cmd = 'python3 -c "{}"'
        python_cmd = ('import os;'
                      'import json;'
                      'return json.dumps(os.stat("{}"))'
                      .format(path))
        cmd.format(python_cmd)
        result = await self.run_command(cmd, target)
        return json.loads(result['Stdout'])

    async def file_contents(self, path, target):
        '''
        Returns the contents of a file

        :param path: File path
        :param target: Unit object or unit name string
        '''
        cmd = 'cat {}'.format(path)
        result = await self.run_command(cmd, target)
        return result['Stdout']
