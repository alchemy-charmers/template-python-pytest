import os
import pytest
import subprocess

# Treat all tests as coroutines
pytestmark = pytest.mark.asyncio

juju_repository = os.getenv('JUJU_REPOSITORY', '.').rstrip('/')
series = ['xenial',
          'bionic',
          pytest.param('cosmic', marks=pytest.mark.xfail(reason='canary')),
          ]
sources = [('local', '{}/builds/${metadata.package}'.format(juju_repository)),
           # ('jujucharms', 'cs:...'),
           ]


# Custom fixtures
@pytest.fixture(params=series)
def series(request):
    return request.param


@pytest.fixture(params=sources, ids=[s[0] for s in sources])
def source(request):
    return request.param


@pytest.fixture
async def app(model, series, source):
    app_name = '${metadata.package}-{}-{}'.format(series, source[0])
    return await model._wait_for_new('application', app_name)


async def test_${fixture}_deploy(model, series, source):
    # Starts a deploy for each series
    # Using subprocess b/c libjuju fails with JAAS
    # https://github.com/juju/python-libjuju/issues/221
    application_name = '${metadata.package}-{}-{}'.format(series, source[0])
    subprocess.check_call(['juju',
                           'deploy',
                           source[1],
                           '-m', model.info.name,
                           application_name,
                           ])


# Tests
async def test_${fixture}_status(model, app):
    # Verifies status for all deployed series of the charm
    await model.block_until(lambda: app.status == 'active')


async def test_example_action(app):
    unit = app.units[0]
    action = await unit.run_action('example-action')
    action = await action.wait()
    assert action.status == 'completed'
