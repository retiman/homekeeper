import homekeeper
import homekeeper.config
import homekeeper.testing
import mock
import unittest

config = homekeeper.config
os = None
patch = mock.patch
shutil = None
testing = homekeeper.testing

class HomekeeperTest(unittest.TestCase):
    def setUp(self):
        global os, shutil
        self.filesystem, os, shutil = testing.init()
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
        self.filesystem.CreateFile(os.path.join(self.home, '.gitconfig'))
        self.homekeeper.track(os.path.join(self.home, '.gitconfig'))
        self.assertEquals(os.path.join(self.config.directory, '.gitconfig'),
                          os.readlink(os.path.join(self.home, '.gitconfig')))

    def test_track_target_that_doesnt_exist(self):
        self.assertFalse(os.path.exists(os.path.join(self.home, '.gitconfig')))
        self.homekeeper.track(os.path.join(self.home, '.gitconfig'))
        self.assertFalse(os.path.exists(os.path.join(self.config.directory,
                                                     '.gitconfig')))
        self.assertFalse(os.path.islink(os.path.join(self.home, '.gitconfig')))

    def test_track_target_that_already_exists(self):
        self.filesystem.CreateFile(os.path.join(self.home, '.gitconfig'))
        self.filesystem.CreateFile(os.path.join(self.config.directory,
                                                '.gitconfig'))
        self.homekeeper.track(os.path.join(self.home, '.gitconfig'))
        self.assertFalse(os.path.islink(os.path.join(self.home, '.gitconfig')))

    def test_init(self):
        os.unlink(testing.configuration_file())
        self.assertFalse(os.path.exists(testing.configuration_file()))
        self.homekeeper = homekeeper.Homekeeper(testing.configuration_file())
        self.homekeeper.init()
        self.assertTrue(os.path.exists(testing.configuration_file()))

    def test_link(self):
        self.filesystem.CreateFile(os.path.join(self.config.base, '.bashrc'))
        self.filesystem.CreateFile(os.path.join(self.config.base, '.vimrc'))
        self.filesystem.CreateFile(os.path.join(self.config.directory,
                                                '.vimrc'))
        self.homekeeper.link()
        self.assertEquals(os.path.join(self.config.base, '.bashrc'),
                          os.readlink(os.path.join(self.home, '.bashrc')))
        self.assertEquals(os.path.join(self.config.directory, '.vimrc'),
                          os.readlink(os.path.join(self.home, '.vimrc')))

    @patch('homekeeper.util.create_symlinks')
    @patch('homekeeper.util.cleanup_symlinks')
    def test_link_with_excludes(self, cleanup_symlinks, create_symlinks):
        self.config.excludes = ['.bashrc']
        self.config.save(testing.configuration_file())
        self.homekeeper = homekeeper.Homekeeper()
        self.filesystem.CreateFile(os.path.join(self.config.base, '.bashrc'))
        self.filesystem.CreateFile(os.path.join(self.home, '.bashrc'))
        self.homekeeper.link()
        create_symlinks.assert_called_with(self.config.directory,
                                           self.home,
                                           excludes=self.config.excludes,
                                           cherrypicks=self.config.cherrypicks)
        cleanup_symlinks.assert_called_with(os.getenv('HOME'))

    @patch('homekeeper.util.create_symlinks')
    @patch('homekeeper.util.cleanup_symlinks')
    def test_link_with_cherrypicks(self, cleanup_symlinks, create_symlinks):
        self.config.cherrypicks = [os.path.join('.foo', 'bar', 'baz')]
        self.config.save(testing.configuration_file())
        self.homekeeper = homekeeper.Homekeeper()
        self.homekeeper.link()
        create_symlinks.assert_called_with(self.config.directory,
                                           self.home,
                                           excludes=self.config.excludes,
                                           cherrypicks=self.config.cherrypicks)
        cleanup_symlinks.assert_called_with(os.getenv('HOME'))

