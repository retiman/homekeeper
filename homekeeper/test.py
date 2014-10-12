import homekeeper
import homekeeper.config
import homekeeper.testing
import unittest

# pylint: disable=invalid-name
os = None
testing = homekeeper.testing

class HomekeeperTest(unittest.TestCase):
    def setUp(self):
        self.filesystem, globals()['os'] = testing.create_fake_filesystem()
        self.config = None
        self.homekeeper = None
        self.home = '/home/johndoe'
        self._configure()

    def tearDown(self):
        del self.filesystem

    def _configure(self):
        os.makedirs(self.home)
        os.makedirs(self.home + '/dotfiles-base')
        os.makedirs(self.home + '/dotfiles-main')
        self.config = homekeeper.config.Config()
        self.config.base = self.home + '/dotfiles-base'
        self.config.directory = self.home + '/dotfiles-main'
        self.config.override = True
        self.config.save(self.home + '/.homekeeper.json')
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

