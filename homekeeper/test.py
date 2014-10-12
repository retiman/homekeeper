import fake_filesystem
import homekeeper
import homekeeper.config
import unittest

# pylint: disable=invalid-name
os = None

class HomekeeperTest(unittest.TestCase):
    def setUp(self):
        # pylint: disable=global-statement
        global os
        self.filesystem = fake_filesystem.FakeFilesystem()
        self.homekeeper = None
        self.home = '/home/johndoe'
        os = fake_filesystem.FakeOsModule(self.filesystem)
        homekeeper.os = os
        homekeeper.util.os = os
        homekeeper.util.os.getenv = lambda var: self.home
        homekeeper.util.shutil.rmtree = os.rmdir

    def tearDown(self):
        del self.filesystem

    def test_link(self):
        config = homekeeper.config.Config()
        config.base = self.home + '/dotfiles-base'
        config.directory = self.home + '/dotfiles-main'
        config.override = True
        config.save()
        self.homekeeper = homekeeper.Homekeeper()
        self.filesystem.CreateFile(config.base + '/.bashrc')
        self.filesystem.CreateFile(config.base + '/.vimrc')
        self.filesystem.CreateFile(config.directory + '/.vimrc')
        self.homekeeper.link()
        self.assertEquals(config.base + '/.bashrc',
                          os.readlink(self.home + '/.bashrc'))
        self.assertEquals(config.directory + '/.vimrc',
                          os.readlink(self.home + '/.vimrc'))

