import fake_filesystem
import homekeeper.config
import json
import unittest

# pylint: disable=invalid-name
os = None
Config = homekeeper.config.Config

class ConfigTest(unittest.TestCase):
    def setUp(self):
        # pylint: disable=global-statement
        global os
        self.config = None
        self.filesystem = fake_filesystem.FakeFilesystem()
        os = fake_filesystem.FakeOsModule(self.filesystem)
        homekeeper.config.os = os
        self.write_configuration()

    def tearDown(self):
        del self.filesystem

    def write_configuration(self):
        config = {
            'base': os.path.join(os.getenv('HOME'), 'dotfiles-base'),
            'directory': os.path.join(os.getenv('HOME'), 'dotfiles-main'),
            'excludes': ['.git'],
            'override': True
        }
        pathname = Config.PATHNAME
        self.filesystem.CreateFile(pathname)
        config_file = open(pathname, 'w')
        config_file.write(json.dumps(config))
        config_file.close()

    def test_defaults_no_configuration_file(self):
        os.unlink(Config.PATHNAME)
        self.config = Config()
        self.assertFalse(os.path.exists(Config.PATHNAME))
        self.assertEquals(self.config.base,
                          Config.DEFAULTS['base'])
        self.assertEquals(self.config.directory,
                          Config.DEFAULTS['directory'])
        self.assertEquals(self.config.excludes,
                          Config.DEFAULTS['excludes'])
        self.assertEquals(self.config.override,
                          Config.DEFAULTS['override'])
