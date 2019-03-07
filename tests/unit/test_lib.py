#!/usr/bin/python3


class TestLib():
    def test_pytest(self):
        assert True

    def test_${fixture}(self, ${fixture}):
        ''' See if the helper fixture works to load charm configs '''
        assert isinstance(${fixture}.charm_config, dict)

    # Include tests for functions in ${libfile}
