import os
import pytest
from juju.model import Model

# Treat tests as coroutines
pytestmark = pytest.mark.asyncio

series = ['xenial', 'bionic']
juju_repository = os.getenv('JUJU_REPOSITORY', '.').rstrip('/')


@pytest.fixture
async def model():
    model = Model()
    await model.connect_current()
    yield model
    await model.disconnect()


@pytest.fixture
async def apps(model):
    apps = []
    for entry in series:
        app = model.applications['${metadata.package}-{}'.format(entry)]
        apps.append(app)
    return apps


@pytest.fixture
async def units(apps):
    units = []
    for app in apps:
        units.extend(app.units)
    return units


@pytest.mark.parametrize('series', series)
async def test_${fixture}_deploy(model, series):
    # Starts a deploy for each series
    await model.deploy('{}/builds/${metadata.package}'.format(juju_repository),
                       series=series,
                       application_name='${metadata.package}-{}'.format(series))
    assert True


async def test_${fixture}_status(apps, model):
    # Verifies status for all deployed series of the charm
    for app in apps:
        await model.block_until(lambda: app.status == 'active')
    assert True


async def test_example_action(units):
    for unit in units:
        action = await unit.run_action('example-action')
        action = await action.wait()
        assert action.status == 'completed'
