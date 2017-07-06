import click.testing
import homekeeper
import homekeeper.cli
import mock
import os


@mock.patch('homekeeper.Homekeeper')
class TestCli(object):
    def setup_method(self):
        self.runner = click.testing.CliRunner()

    def test_clean(self, mock):
        args = ['clean']
        result = self.runner.invoke(homekeeper.cli.main, args)
        assert result.output == ''
        assert result.exit_code == 0
        assert mock.called_once_with(args[0])
        assert mock.clean.called_once()

    def test_init_with_custom_config(self, mock):
        dotfiles_directory = os.getcwd()
        custom_homekeeper_json = os.path.join(dotfiles_directory,
                                              '.config.json')
        args = ['--config-path', custom_homekeeper_json, 'init']
        result = self.runner.invoke(homekeeper.cli.main, args)
        assert result.output == ''
        assert result.exit_code == 0
        assert mock.called_once_with(config_path=custom_homekeeper_json,
                                     cleanup_symlinks=False, overwrite=False)
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
