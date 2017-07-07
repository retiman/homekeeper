import click.testing
import homekeeper
import homekeeper.cli
import mock
import os


class TestCli(object):
    def setup_method(self):
        self.runner = click.testing.CliRunner()
        self.mock_instance = mock.MagicMock()
        self.patcher = mock.patch('homekeeper.Homekeeper')
        self.mock_class = self.patcher.start()
        self.mock_class.return_value = self.mock_instance

    def teardown_method(self):
        self.patcher.stop()

    def run(self, *args):
        result = self.runner.invoke(homekeeper.cli.main, args)
        assert result.output == ''
        assert result.exit_code == 0

    def test_cleanup(self):
        self.run('cleanup')
        self.mock_class.cleanup.assert_called_once()
        assert self.mock_instance.cleanup_symlinks == True
        assert self.mock_instance.overwrite == False

    def test_cleanup_ignores_no_cleanup_and_overwrite(self):
        self.run('--no-cleanup', '--overwrite', 'cleanup')
        self.mock_class.cleanup.assert_called_once()
        assert self.mock_instance.cleanup_symlinks == True
        assert self.mock_instance.overwrite == False

    def test_init_with_custom_config(self):
        dotfiles_directory = os.getcwd()
        config_path = os.path.join(dotfiles_directory, '.config.json')
        self.run('--config-path', config_path, 'init')
        self.mock_class.init.assert_called_once()
        self.mock_class.assert_called_once_with(config_path=config_path)
        assert self.mock_instance.cleanup_symlinks == False
        assert self.mock_instance.overwrite == False

    def test_init_cannot_cleanup_or_overwrite(self):
        self.run('--cleanup', '--overwrite', 'init')
        self.mock_class.init.assert_called_once()
        self.mock_class.assert_called_once_with(config_path=None)
        assert self.mock_instance.cleanup_symlinks == False
        assert self.mock_instance.overwrite == False

    def test_keep_with_default_options(self):
        self.run('keep')
        self.mock_class.keep.assert_called_once()
        self.mock_class.assert_called_once_with(config_path=None)
        assert self.mock_instance.cleanup_symlinks == True
        assert self.mock_instance.overwrite == True
