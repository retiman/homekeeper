import fake_filesystem
import homekeeper.config
import json
import unittest
import __builtin__

# pylint: disable=invalid-name
os = None
Config = homekeeper.config.Config

class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.filesystem = fake_filesystem.FakeFilesystem()
        globals()['os'] = fake_filesystem.FakeOsModule(self.filesystem)
        __builtin__.open = fake_filesystem.FakeFileOpen(self.filesystem)
        self.pathname = os.path.join(os.getenv('HOME'), 'homekeeper.json')
        self.defaults = {
            'base': os.path.join(os.getenv('HOME'), 'dotfiles-base'),
            'directory': os.path.join(os.getenv('HOME'), 'dotfiles-main'),
            'excludes': ['.git'],
            'override': True
        }
        self.create_config_file()
        homekeeper.config.os = os

    def tearDown(self):
        del self.filesystem

    def create_config_file(self):
        if os.path.exists(self.pathname):
            self.filesystem.RemoveObject(self.pathname)
        contents = json.dumps(self.defaults)
        self.filesystem.CreateFile(self.pathname, contents=contents)

    def test_defaults(self):
        """Tests creating a Config object with specifying a filename."""
        config = Config()
        self.assertFalse(os.path.exists(Config.PATHNAME))
        self.assertEquals(config.base, Config.DEFAULTS['base'])
        self.assertEquals(config.directory, Config.DEFAULTS['directory'])
        self.assertEquals(config.excludes, Config.DEFAULTS['excludes'])
        self.assertEquals(config.override, Config.DEFAULTS['override'])

    def test_configuration_file(self):
        """Tests creating a Config object with a filename."""
        config = Config(self.pathname)
        self.assertEquals(config.base, self.defaults['base'])
        self.assertEquals(config.excludes, self.defaults['excludes'])
        self.assertEquals(config.override, self.defaults['override'])
        self.assertEquals(config.directory, self.defaults['directory'])

    def test_dotfiles_directory_key_overrides(self):
        """Tests that the old 'dotfiles_directory' key.

        It should override the 'directory' key if present."""
        dotfiles_directory = os.path.join(os.getenv('HOME'), 'dotfiles')
        self.defaults['dotfiles_directory'] = dotfiles_directory
        self.create_config_file()
        config = Config(self.pathname)
        self.assertNotEquals(config.directory, self.defaults['directory'])
        self.assertEquals(config.directory, self.defaults['dotfiles_directory'])

    def test_home_directory_not_allowed(self):
        """Tests that using the home directory is not allowed."""
        self.defaults['directory'] = os.getenv('HOME')
        self.create_config_file()
        config = Config(self.pathname)
        self.assertEquals(config.directory, Config.DEFAULTS['directory'])

    def test_save(self):
        """Tests save config file functionality."""
        pathname = os.path.join(os.getenv('HOME'), 'saved.json')
        config = Config(self.pathname)
        config.excludes = []
        config.override = True
        config.save(pathname)
        config = Config(pathname)
        self.assertEquals(config.excludes, [])
        self.assertEquals(config.override, True)

    def test_save_with_no_pathname(self):
        """Tests save config file without an explicit pathname."""
        config = Config(self.pathname)
        config.excludes = []
        config.save()
        config = Config(self.pathname)
        self.assertEquals(config.excludes, [])
        config = Config()
        config.excludes = ['.git']
        config.save()
        config = Config(Config.PATHNAME)
        self.assertEquals(config.excludes, ['.git'])

