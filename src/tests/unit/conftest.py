#!/usr/bin/python3
import pytest
import mock


@pytest.fixture
def mock_layers(monkeypatch):
    import sys
    sys.modules["charms.layer"] = mock.Mock()
    sys.modules["reactive"] = mock.Mock()
    # Mock any functions in layers that need to be mocked here

    def options(layer):
        # mock options for layers here
        if layer == 'example-layer':
            options = {'port': 9999}
            return options
        else:
            return None

    monkeypatch.setattr('${libfile}.layer.options', options)


@pytest.fixture
def mock_hookenv_config(monkeypatch):
    import yaml

    def mock_config():
        cfg = {}
        yml = yaml.load(open('./config.yaml'))

        # Load all defaults
        for key, value in yml['options'].items():
            cfg[key] = value['default']

        # Manually add cfg from other layers
        # cfg['my-other-layer'] = 'mock'
        return cfg

    monkeypatch.setattr('${libfile}.hookenv.config', mock_config)


@pytest.fixture
def mock_remote_unit(monkeypatch):
    monkeypatch.setattr('${libfile}.hookenv.remote_unit', lambda: 'unit-mock/0')


# Example mocking a subprocess call
# @pytest.fixture
# def mock_ports(monkeypatch, open_ports=''):
#     def mports(*args, **kwargs):
#         if args[0][0] == "opened-ports":
#             return bytes(mports.open_ports, encoding='utf8')
#         elif args[0][0] == "open-port":
#             if args[0][1].lower() not in mports.open_ports:
#                 mports.open_ports = mports.open_ports + args[0][1].lower() + '\n'
#             return bytes(mports.open_ports, encoding='utf8')
#         elif args[0][0] == "close-port":
#             mports.open_ports = mports.open_ports.replace(args[0][1].lower() + '\n', '')
#             return bytes(mports.open_ports, encoding='utf8')
#         else:
#             print("subprocess called with: {}".format(args[0]))
#             return None
#     mports.open_ports = open_ports
#
#     monkeypatch.setattr('${libfile}.subprocess.check_output', mports)
#     monkeypatch.setattr('${libfile}.subprocess.check_call', mports)


@pytest.fixture
def mock_charm_dir(monkeypatch):
    monkeypatch.setattr('${libfile}.hookenv.charm_dir', lambda: '/mock/charm/dir')


@pytest.fixture
def ${fixture}(tmpdir,
               mock_layers,
               mock_hookenv_config,
               mock_charm_dir,
               monkeypatch):
    from $libfile import $libclass
    helper = ${libclass}()

    # Example config file patching
    cfg_file = tmpdir.join("example.cfg")
    with open('./tests/unit/example.cfg', 'r') as src_file:
        cfg_file.write(src_file.read())
    helper.example_config_file = cfg_file.strpath

    # Any other functions that load helper will get this version
    monkeypatch.setattr('${libfile}.${libclass}', lambda: helper)

    return helper
