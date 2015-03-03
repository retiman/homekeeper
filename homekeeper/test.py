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
        self.filesystem.CreateFile(os.path.join(self.home, '.gitconfig'))
        self.homekeeper.track(os.path.join(self.home, '.gitconfig'))
        self.assertEquals(os.path.join(self.config.directory, '.gitconfig'),
                          os.readlink(os.path.join(self.home, '.gitconfig')))

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

    def test_link_with_excludes(self):
        self.config.excludes = ['.bashrc']
        self.config.save(testing.configuration_file())
        self.homekeeper = homekeeper.Homekeeper()
        self.filesystem.CreateFile(os.path.join(self.config.base, '.bashrc'))
        self.filesystem.CreateFile(os.path.join(self.home, '.bashrc'))
        self.homekeeper.link()
        self.assertFalse(os.path.islink(os.path.join(self.home, '.bashrc')),
                         msg='The excluded file was symlinked anyways.')

    def test_link_with_includes(self):
        self.config.includes = [os.path.join('.foo', 'bar', 'baz')]
        self.config.save(testing.configuration_file())
        self.homekeeper = homekeeper.Homekeeper()
        self.filesystem.CreateFile(os.path.join(self.config.base,
                                                '.foo',
                                                'bar',
                                                'baz'))
        self.filesystem.CreateFile(os.path.join(self.home,
                                                '.foo',
                                                'bar',
                                                'unrelated'))
        self.homekeeper.link()
        self.assertFalse(os.path.islink(os.path.join(self.home, '.foo')),
                         msg='The directory was symlinked anyways.')
        self.assertTrue(os.path.islink(os.path.join(self.home,
                                                    '.foo',
                                                    'bar',
                                                    'baz')))
        self.assertTrue(os.path.exists(os.path.join(self.home,
                                                    '.foo',
                                                    'bar',
                                                    'unrelated')))
        self.assertFalse(os.path.islink(os.path.join(self.home,
                                                     '.foo',
                                                     'bar',
                                                     'unrelated')))

