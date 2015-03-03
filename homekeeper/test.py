import homekeeper
import homekeeper.config
import homekeeper.testing
import unittest

# pylint: disable=invalid-name
config = homekeeper.config
os = None
testing = homekeeper.testing

class HomekeeperTest(unittest.TestCase):
    def setUp(self):
        self.filesystem, globals()['os'] = testing.init()
        self.config = None
        self.homekeeper = None
        self.home = os.getenv('HOME')
        self._configure()

    def tearDown(self):
        del self.filesystem

    def _configure(self):
        self.config = config.Config()
        self.config.base = testing.base_directory()
        self.config.directory = testing.main_directory()
        self.config.override = True
        self.config.save(testing.configuration_file())
        self.homekeeper = homekeeper.Homekeeper()

    def test_track(self):
        self.filesystem.CreateFile(self.home + '/.gitconfig')
        self.homekeeper.track(self.home + '/.gitconfig')
        self.assertEquals(self.config.directory + '/.gitconfig',
                          os.readlink(self.home + '/.gitconfig'))

    def test_link(self):
        self.filesystem.CreateFile(self.config.base + '/.bashrc')
        self.filesystem.CreateFile(self.config.base + '/.vimrc')
        self.filesystem.CreateFile(self.config.directory + '/.vimrc')
        self.homekeeper.link()
        self.assertEquals(self.config.base + '/.bashrc',
                          os.readlink(self.home + '/.bashrc'))
        self.assertEquals(self.config.directory + '/.vimrc',
                          os.readlink(self.home + '/.vimrc'))

