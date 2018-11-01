#!/usr/bin/python3

import pytest
from juju.model import Model

# Treat tests as coroutines
pytestmark = pytest.mark.asyncio


@pytest.fixture
async def model():
    model = Model()
    await model.connect_current()
    yield model
    await model.disconnect()


@pytest.fixture
async def ${fixture}_app(model):
    app = await model.deploy('local:', series='bionic')
    await model.block_until(lambda: app.status == 'active')
    return app


async def test_deploy(${fixture}_app):
    assert True

# def test_example_action(self, deploy, unit):
#     uuid = unit.run_action('example-action')
#     action_output = deploy.get_action_output(uuid, full_output=True)
#     print(action_output)
#     assert action_output['status'] == 'completed'
