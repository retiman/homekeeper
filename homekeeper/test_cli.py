import click.testing
import homekeeper
import homekeeper.cli
import mock
import os


@mock.patch('homekeeper.Homekeeper')
class TestCli(object):
    def setup_method(self):
        self.runner = click.testing.CliRunner()

    def test_init_with_custom_config(self, mock):
        custom_directory = os.getcwd()
        args = ['init', custom_directory]
        result = self.runner.invoke(homekeeper.cli.main, args)
        assert result.output == ''
        assert result.exit_code == 0
        assert mock.called_once_with(args[0])
        assert mock.init.called_once()

    def test_init_with_no_config(self, mock):
        args = ['init']
        result = self.runner.invoke(homekeeper.cli.main, args)
        assert result.output == ''
        assert result.exit_code == 0
        assert mock.called_once_with()
        assert mock.init.called_once()

    #def test_keep_with_default_option(self, mock):
    #    args = ['keep']
    #    self.runner.invoke(homekeeper.cli.main, args)
    #    assert mock.called_once_with()
    #    assert mock.init.called_once()
