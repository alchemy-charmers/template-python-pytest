# Overview
This is a template for writing charms with unit and functional testing included
from the start. It is meant to provide a quick start to creating a charm and
encourage testing from the beginning.

## Building
The template comes out of the box with a build script that will build the charm.
There are empty folders for interfaces, layers, and the charm source. Interfaces
and Layers are pulled from upstream but this template recommends adding subrepos
in the appropriate folder to the charm to allow tracking of versions for
interfaces and layers. If an interface or layers is present in the folder it
will be used instead of the upstream.

To build simply run the script
```bash
./build.sh
```

## Testing
Testing is done via tox and there are two environments setup one for unit and
one for functional testing. Each has a separate requirements file to setup the
virtualenv that they will be run in. These are for test only requirements.

## Unit testing
The unit testing is performed via pytest. Test are defined in the folder
/tests/unit/ in the test_XXX.py

To run unit test with tox run:
```bash
tox -e unit
```

Out of the gate, unit testing just verifies that the testing framework is
working. It is recommend that the library file in the lib folder be fully unit
tested.

## Functional testing

### Libjuju
The currently supported method of functional testing uses libjuju to interact
with juju and the units. The legacy method is only included until libjuju has
some maturity as it has only recently been added to the template.

To run libjuju functional testing:
```bash
tox -e functional
```
This requires a controller and model be available to run the test in.

### Legacy
The legacy testing relies on amulet testing, which has become outdated. It still
works but it would be preferable to look at moving to libjuju to remove the
dependency.

Amulet testing is run with tox via:
```bash
tox -e amulet
```

Note that amulet tests require installing the jujudeployer which can be
installed via:
```bash
pip install bundletester
```
This will eventually be depreciated for libjuju
