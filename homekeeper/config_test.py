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
        self.filesystem = ConfigTest.create_fake_filesystem()
        self.pathname = os.path.join(os.getenv('HOME'), 'homekeeper.json')
        self.defaults = {
            'base': os.path.join(os.getenv('HOME'), 'dotfiles-base'),
            'directory': os.path.join(os.getenv('HOME'), 'dotfiles-main'),
            'dotfiles_directory': os.path.join(os.getenv('HOME'), 'dotfiles'),
            'excludes': ['.git'],
            'override': True
        }
        self.filesystem.CreateFile(self.pathname,
                                   contents=json.dumps(self.defaults))
        homekeeper.config.os = os

    def tearDown(self):
        del self.filesystem

    @staticmethod
    def create_fake_filesystem():
        filesystem = fake_filesystem.FakeFilesystem()
        globals()['os'] = fake_filesystem.FakeOsModule(filesystem)
        __builtin__.open = fake_filesystem.FakeFileOpen(filesystem)
        return filesystem

    def test_defaults(self):
        config = Config()
        self.assertFalse(os.path.exists(Config.PATHNAME))
        self.assertEquals(config.base, Config.DEFAULTS['base'])
        self.assertEquals(config.directory, Config.DEFAULTS['directory'])
        self.assertEquals(config.excludes, Config.DEFAULTS['excludes'])
        self.assertEquals(config.override, Config.DEFAULTS['override'])

    def test_configuration(self):
        config = Config(self.pathname)
        self.assertEquals(config.base, self.defaults['base'])
        self.assertEquals(config.excludes, self.defaults['excludes'])
        self.assertEquals(config.override, self.defaults['override'])
        self.assertEquals(config.directory, self.defaults['dotfiles_directory'])
        self.assertNotEquals(config.directory, self.defaults['directory'])
