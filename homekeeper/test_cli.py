import click.testing
import homekeeper
import homekeeper.cli
import mock
import os


@mock.patch('homekeeper.Homekeeper')
class TestCli(object):
    def setup_method(self):
        self.runner = click.testing.CliRunner()

    def run(self, *args):
        result = self.runner.invoke(homekeeper.cli.main, args)
        assert result.output == ''
        assert result.exit_code == 0

    def test_cleanup(self, MockHomekeeper):
        self.run('cleanup')
        MockHomekeeper.cleanup.assert_called_once()
        MockHomekeeper.assert_called_once_with(cleanup_symlinks=True)

    def test_clean_ignores_no_cleanup(self, MockHomekeeper):
        self.run('--no-cleanup', 'cleanup')
        MockHomekeeper.assert_called_once_with(cleanup_symlinks=True)
        MockHomekeeper.cleanup.assert_called_once()

    def test_init_with_custom_config(self, MockHomekeeper):
        dotfiles_directory = os.getcwd()
        config_path = os.path.join(dotfiles_directory, '.config.json')
        self.run('--config-path', config_path, 'init')
        MockHomekeeper.init.assert_called_once()
        MockHomekeeper.assert_called_once_with(config_path=config_path,
                                               cleanup_symlinks=False,
                                               overwrite=False)

    def test_init_cannot_cleanup_or_overwrite(self, MockHomekeeper):
        self.run('--cleanup', '--overwrite', 'init')
        MockHomekeeper.init.assert_called_once()
        MockHomekeeper.assert_called_once_with(config_path=None,
                                               cleanup_symlinks=False,
                                               overwrite=False)

    def test_keep_with_default_options(self, MockHomekeeper):
        self.run('keep')
        MockHomekeeper.keep.assert_called_once()
        MockHomekeeper.assert_called_once_with(config_path=None,
                                               cleanup_symlinks=True,
                                               overwrite=True)
