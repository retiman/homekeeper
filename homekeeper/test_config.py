import homekeeper.config
import homekeeper.testing
import json

os = None
shutil = None
testing = homekeeper.testing
Config = homekeeper.config.Config

class TestConfig(object):
    def setup_method(self):
        global os, shutil
        self.filesystem, os, shutil = testing.init()
        self.defaults = {
            'base': testing.base_directory(),
            'directory': testing.main_directory(),
            'excludes': ['.git'],
            'override': True
        }
        self.create_config_file()

    def teardown_method(self):
        del self.filesystem

    def create_config_file(self):
        if os.path.exists(testing.configuration_file()):
            self.filesystem.RemoveObject(testing.configuration_file())
        contents = json.dumps(self.defaults)
        self.filesystem.CreateFile(testing.configuration_file(),
                                   contents=contents)

    def test_defaults(self):
        """Tests creating a Config object without specifying a filename."""
        config = Config()
        assert not os.path.exists(Config.PATHNAME)
        assert config.base == Config.DEFAULTS['base']
        assert config.directory == Config.DEFAULTS['directory']
        assert config.excludes == Config.DEFAULTS['excludes']
        assert config.cherrypicks == Config.DEFAULTS['cherrypicks']
        assert config.override == Config.DEFAULTS['override']

    def test_invalid_configuration_file(self):
        self.filesystem.CreateFile('homekeeper.json', contents='invalid-json')
        config = Config('homekeeper.json')
        assert config.base == Config.DEFAULTS['base']
        assert config.directory == Config.DEFAULTS['directory']
        assert config.excludes == Config.DEFAULTS['excludes']
        assert config.cherrypicks == Config.DEFAULTS['cherrypicks']
        assert config.override == Config.DEFAULTS['override']

    def test_configuration_file(self):
        """Tests creating a Config object with a filename."""
        config = Config(testing.configuration_file())
        assert config.base == self.defaults['base']
        assert config.excludes == self.defaults['excludes']
        assert config.override == self.defaults['override']
        assert config.directory == self.defaults['directory']

    def test_dotfiles_directory_key_overrides(self):
        """Tests that the old 'dotfiles_directory' key should override the
        'directory' key if present."""
        self.defaults['dotfiles_directory'] = testing.dotfiles_directory()
        self.create_config_file()
        config = Config(testing.configuration_file())
        assert config.directory != self.defaults['directory']
        assert config.directory == self.defaults['dotfiles_directory']

    def test_home_directory_not_allowed(self):
        """Tests that using the home directory as a base is not allowed."""
        self.defaults['directory'] = os.getenv('HOME')
        self.create_config_file()
        config = Config(testing.configuration_file())
        assert config.directory == Config.DEFAULTS['directory']

    def test_save(self):
        """Tests saving a config file."""
        pathname = os.path.join(os.getenv('HOME'), 'saved.json')
        config = Config(testing.configuration_file())
        config.excludes = []
        config.override = True
        config.save(pathname)
        config = Config(pathname)
        assert config.excludes == []
        assert config.override

    def test_save_with_no_pathname(self):
        """Tests saving config file without an explicit pathname."""
        config = Config(testing.configuration_file())
        config.excludes = []
        config.save()
        config = Config(testing.configuration_file())
        assert config.excludes == []
