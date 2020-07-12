import os
import pytest
import homekeeper.config
import homekeeper.exceptions
import homekeeper.lib
import homekeeper.testing


config = homekeeper.config
fopen = homekeeper.lib.fopen
testing = homekeeper.testing
ConfigData = homekeeper.config.ConfigData
ConfigException = homekeeper.exceptions.ConfigException


class ConfigTest:
    def get_module_directory(self):
        return os.path.dirname(__file__)

    def get_data(self, *args):
        return os.path.join(self.get_module_directory(), *args)

    def test_read(self):
        config_file = self.get_data('testdata', 'ConfigTest.test_read')
        config_data = config.read(config_file)
        assert config_data.directories == [
            '/home/johndoe/dotfiles/desktop',
            '/home/johndoe/dotfiles/laptop',
        ]
        assert config_data.excludes == [
            '.git',
            'README.md'
        ]

    def test_read_directory(self):
        config_file = self.get_data('testdata', 'ConfigTest.test_read_directory')
        config_data = config.read(config_file)
        assert config_data.directories == ['/home/johndoe/dotfiles']

    def test_read_single_directory(self):
        config_file = self.get_data('testdata', 'ConfigTest.test_read_single_directory')
        config_data = config.read(config_file)
        assert config_data.directories == ['/home/johndoe/dotfiles']

    def test_read_invalid_single_directory(self):
        config_file = self.get_data('testdata', 'ConfigTest.test_read_invalid_single_directory')
        with pytest.raises(ConfigException):
            config.read(config_file)

    def test_read_invalid_directories(self):
        config_file = self.get_data('testdata', 'ConfigTest.test_read_invalid_directories')
        with pytest.raises(ConfigException):
            config.read(config_file)

    def test_read_invalid_excludes(self):
        config_file = self.get_data('testdata', 'ConfigTest.test_read_invalid_excludes')
        with pytest.raises(ConfigException):
            config.read(config_file)

    def test_read_invalid_exclude(self):
        config_file = self.get_data('testdata', 'ConfigTest.test_read_invalid_single_exclude')
        with pytest.raises(ConfigException):
            config.read(config_file)

    def test_read_invalid_file_with_bad_decoding(self):
        config_file = self.get_data('testdata', 'ConfigTest.test_read_file_with_bad_decoding')
        with pytest.raises(ConfigException):
            config.read(config_file)

    def test_read_missing_file(self):
        config_file = self.get_data('testdata', 'ConfigTest.test_read_missing_file')
        with pytest.raises(ConfigException):
            config.read(config_file)

    def test_read_with_both_directory_and_directories_fails(self):
        # TODO: Implement me!
        pass

    def test_read_directory_with_non_str_value_fails(self):
        # TODO: Implement me!
        pass

    def test_write(self, tmpdir):
        config_data = ConfigData()
        config_data.directories = ['/home/johndoe/dotfiles']
        config_data.excludes = ['.git']
        config_file = config.write(config_data, os.path.join(tmpdir.strpath, 'homekeeper.json'))
        with fopen(config_file) as f:
            actual = f.read()
        with fopen(os.path.join(self.get_module_directory(), 'testdata', 'ConfigTest.test_write')) as f:
            expected = f.read()
        assert actual == expected
