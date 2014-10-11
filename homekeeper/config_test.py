import fake_filesystem
import homekeeper.config
import unittest

# pylint: disable=invalid-name
os = None
config = homekeeper.config

class ConfigTest(unittest.TestCase):
    def setUp(self):
        # pylint: disable=global-statement
        global os
        self.config = None
        self.filesystem = fake_filesystem.FakeFilesystem()
        os = fake_filesystem.FakeOsModule(self.filesystem)
        homekeeper.config.os = os

    def tearDown(self):
        del self.filesystem

    def test_defaults_no_configuration_file(self):
        self.config = config.Config()
        self.assertEquals(self.config.base,
                          config.Config.DEFAULTS['base'])
        self.assertEquals(self.config.directory,
                          config.Config.DEFAULTS['directory'])
        self.assertEquals(self.config.excludes,
                          config.Config.DEFAULTS['excludes'])
        self.assertEquals(self.config.override,
                          config.Config.DEFAULTS['override'])
