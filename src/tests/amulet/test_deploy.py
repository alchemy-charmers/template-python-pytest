#!/usr/bin/python3

import pytest
import amulet
import requests
import time


@pytest.fixture(scope="module")
def deploy():
    deploy = amulet.Deployment(series='bionic')
    deploy.add('${metadata.package.lower()}')
    deploy.setup(timeout=900)
    deploy.sentry.wait()
    return deploy


@pytest.fixture(scope="module")
def unit(deploy):
    return deploy.sentry['${metadata.package.lower()}'][0]

# An example fixture to set a config for a single test
# @pytest.fixture()
# def tmpcfg(deploy):
#     print("Setting cfg")
#     deploy.configure('${metadata.package.lower()}', {'example-cfg': False})
#     time.sleep(10)
#     yield  # The test will run here
#     print("Returning to default")
#     deploy.configure('${metadata.package.lower()}', {'example-cfg': True})
#     time.sleep(10)


class Test${libclass}():

    def test_amulet(self, deploy):
        assert True


    def test_example_action(self, deploy, unit):
          uuid = unit.run_action('example-action')
          action_output = deploy.get_action_output(uuid, full_output=True)
          print(action_output)
          assert action_output['status'] == 'completed'

        # test we can access over http
        # page = requests.get('http://{}'.format(self.unit.info['public-address']))
        # self.assertEqual(page.status_code, 200)
        # Now you can use self.d.sentry[SERVICE][UNIT] to address each of the units and perform
        # more in-depth steps. Each self.d.sentry[SERVICE][UNIT] has the following methods:
        # - .info - An array of the information of that unit from Juju
        # - .file(PATH) - Get the details of a file on that unit
        # - .file_contents(PATH) - Get plain text output of PATH file from that unit
        # - .directory(PATH) - Get details of directory
        # - .directory_contents(PATH) - List files and folders in PATH on that unit
        # - .relation(relation, service:rel) - Get relation data from return service
