import click.testing
import homekeeper
import homekeeper.cli
import mock
import os


@mock.patch('homekeeper.Homekeeper')
class TestCli(object):
    def setup_method(self):
        self.runner = click.testing.CliRunner()

    def verify_run_success(self, *args):
        result = self.runner.invoke(homekeeper.cli.main, args)
        assert result.output == ''
        assert result.exit_code == 0

    def test_clean(self, MockHomekeeper):
        self.verify_run_success('clean')
        MockHomekeeper.assert_called_once_with(cleanup_symlinks=True)
        MockHomekeeper.cleanup.assert_called_once()

    def test_init_with_custom_config(self, MockHomekeeper):
        dotfiles_directory = os.getcwd()
        config_path = os.path.join(dotfiles_directory,'.config.json')
        self.verify_run_success('--config-path', config_path, 'init')
        MockHomekeeper.assert_called_once_with(config_path=config_path,
                                               cleanup_symlinks=False,
                                               overwrite=False)
        MockHomekeeper.init.assert_called_once()

    def test_init_cannot_cleanup_or_overwrite(self, MockHomekeeper):
        self.verify_run_success('--cleanup', '--overwrite', 'init')
        MockHomekeeper.assert_called_once_with(config_path=None,
                                               cleanup_symlinks=False,
                                               overwrite=False)
        MockHomekeeper.init.assert_called_once()

    # def test_keep_with_default_option(self, mock):
    #     args = ['keep']
    #     self.runner.invoke(homekeeper.cli.main, args)
    #     assert mock.called_once_with()
    #     assert mock.init.called_once()
