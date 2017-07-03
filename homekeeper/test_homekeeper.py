import homekeeper
import homekeeper.config
import homekeeper.testing
import mock

config = homekeeper.config
os = None
patch = mock.patch
shutil = None
testing = homekeeper.testing

class TestHomekeeper():
    def setup_method(self):
        global os, shutil
        self.filesystem, os, shutil = testing.init()
        self.config = None
        self.homekeeper = None
        self.home = os.getenv('HOME')
        self._configure()

    def teardown_method(self):
        del self.filesystem

    def _configure(self):
        self.config = config.Config()
        self.config.base = testing.base_directory()
        self.config.directory = testing.main_directory()
        self.config.override = True
        self.config.save(testing.configuration_file())
        self.homekeeper = homekeeper.Homekeeper()

    def test_init(self):
        os.unlink(testing.configuration_file())
        assert not os.path.exists(testing.configuration_file())
        self.homekeeper = homekeeper.Homekeeper(testing.configuration_file())
        self.homekeeper.init()
        assert os.path.exists(testing.configuration_file())

    def test_link(self):
        self.filesystem.CreateFile(os.path.join(self.config.base, '.bashrc'))
        self.filesystem.CreateFile(os.path.join(self.config.base, '.vimrc'))
        self.filesystem.CreateFile(os.path.join(self.config.directory,
                                                '.vimrc'))
        self.homekeeper.link()
        expected = os.path.join(self.config.base, '.bashrc')
        result = os.readlink(os.path.join(self.home, '.bashrc'))
        assert expected == result
        expected = os.path.join(self.config.directory, '.vimrc')
        result = os.readlink(os.path.join(self.home, '.vimrc'))
        assert expected == result

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
                                           excludes=self.config.excludes)
        cleanup_symlinks.assert_called_with(os.getenv('HOME'))
