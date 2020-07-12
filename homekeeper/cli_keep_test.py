import homekeeper.config
import homekeeper.testing


config = homekeeper.config
lib = homekeeper.lib
BaseCliTest = homekeeper.testing.BaseCliTest
ConfigData = homekeeper.config.ConfigData


# pylint: disable=unused-argument
class CliKeepTest(BaseCliTest):
    def test_keep(self, os, files, directories):
        config.write(self.config_data)
        result = self.run('--debug', 'keep')
        assert result.exit_code == 0

    def test_keep_without_cleanup(self, os, files, directories):
        config.write(self.config_data)
        result = self.run('--debug', '--no-cleanup-symlinks', 'keep')
        # TODO: Add assertions for no cleanup
        assert result.exit_code == 0

    def test_keep_without_overwriting(self, os, files, directories):
        config.write(self.config_data)
        result = self.run('--debug', '--no-overwrite', 'keep')
        # TODO: Add assertions for no no overwrite
        assert result.exit_code == 0

    def test_keep_with_different_config_path(self, os, files, directories):
        lib.makedirs(self.home_directory, 'config')
        config_file = os.path.join(self.home_directory, 'config', '.homekeeper.json')
        config.write(self.config_data, config_file)
        result = self.run('--debug', "--config-path={}".format(config_file), 'keep')
        assert result.exit_code == 0

    def test_keep_with_multiple_source_directories(self, os, files, directories):
        dotfiles_1 = os.path.join(self.home_directory, 'dotfiles')
        dotfiles_2 = os.path.join(self.home_directory, 'dotfiles2')
        lib.makedirs(dotfiles_1)
        lib.makedirs(dotfiles_2)
        self.config_data.directories = [str(pathname) for pathname in [dotfiles_1, dotfiles_2]]
        config.write(self.config_data)
        result = self.run('--debug', 'keep')
        assert result.exit_code == 0
