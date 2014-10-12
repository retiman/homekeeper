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
        os = fake_filesystem.FakeOsModule(self.filesystem)
        homekeeper.os = os
        homekeeper.util.os = os
        homekeeper.util.shutil.rmtree = os.rmdir
        self.config = homekeeper.config.Config()
        self.homekeeper = None

    def tearDown(self):
        del self.filesystem

    def test_link(self):
        home = '/home/johndoe'
        source = home + '/dotfiles/.vimrc'
        target = home + '/.vimrc'
        homekeeper.util.os.getenv = lambda var: home
        self.config.directory = home + '/dotfiles'
        self.config.save()
        self.homekeeper = homekeeper.Homekeeper()
        self.filesystem.CreateFile(source)
        self.assertTrue(os.path.exists(source))
        self.assertFalse(os.path.exists(target))
        self.homekeeper.link()
        self.assertTrue(os.path.exists(source))
        self.assertTrue(os.path.exists(target))
        self.assertTrue(os.path.islink(target))
        self.assertEquals(source, os.readlink(target))
