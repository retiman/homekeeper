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

    def test_cleanup(self, MockHomekeeper):
        self.verify_run_success('cleanup')
        MockHomekeeper.assert_called_once_with(cleanup_symlinks=True)
        MockHomekeeper.cleanup.assert_called_once()

    def test_clean_ignores_no_cleanup(self, MockHomekeeper):
        self.verify_run_success('--no-cleanup', 'cleanup')
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

    def test_keep_with_default_options(self, MockHomekeeper):
        self.verify_run_success('keep')
        MockHomekeeper.assert_called_once_with(config_path=None,
                                               cleanup_symlinks=True,
                                               overwrite=True)
        MockHomekeeper.keep.assert_called_once()
