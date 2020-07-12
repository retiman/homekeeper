import homekeeper.testing


lib = homekeeper.lib
BaseCliTest = homekeeper.testing.BaseCliTest


class CliVersionTest(BaseCliTest):
    def test_version(self):
        result = self.run('version')
        assert result.exit_code == 0
        assert result.output == "homekeeper version {}\n".format(homekeeper.__version__)
