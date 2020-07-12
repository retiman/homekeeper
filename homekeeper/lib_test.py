import homekeeper.lib
import homekeeper.testing


cd = homekeeper.lib.cd
lib = homekeeper.lib
BaseFakeFilesystemTest = homekeeper.testing.BaseFakeFilesystemTest


class LibTest(BaseFakeFilesystemTest):
    def test_change_directory(self, os):
        current_directory = os.getcwd()
        directory = os.path.join(os.sep, 'foo', 'bar')
        lib.makedirs(directory)
        with cd(directory):
            assert os.getcwd() == directory
        assert os.getcwd() == current_directory

    def test_remove_directory(self, fopen, os):
        directory = os.path.join(os.sep, 'foo', 'bar')
        lib.makedirs(directory)
        with fopen(os.path.join(directory, 'file.txt'), 'w') as f:
            f.write('hello!')
        assert os.path.exists(directory)
        lib.remove(directory)
        assert not os.path.exists(directory)

    def test_makedirs_does_not_raise(self, os):
        directory = os.path.join(os.sep, 'foo', 'bar')
        lib.makedirs(directory)
        assert os.path.exists(directory)
        lib.makedirs(directory)
        assert os.path.exists(directory)

    def test_get_home_directory(self, os):
        assert os.getenv('HOME') == os.path.join(os.sep, 'home', 'johndoe')

    def test_remove_file_or_symlink(self, os):
        source = os.path.join(self.home_directory, '.bashrc')
        target = os.path.join(self.home_directory, '.bash_profile')
        os.symlink(source, target)
        lib.remove(source)
        lib.remove(target)
        assert not os.path.exists(source)
        assert not os.path.exists(target)
