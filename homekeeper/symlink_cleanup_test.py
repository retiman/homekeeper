import homekeeper.lib
import homekeeper.symlink
import homekeeper.testing


cd = homekeeper.lib.cd
lib = homekeeper.lib
symlink = homekeeper.symlink
BaseFakeFilesystemTest = homekeeper.testing.BaseFakeFilesystemTest


class SymlinkCleanupTest(BaseFakeFilesystemTest):
    def test_cleanup_symlinks(self, os):
        lib.touch(self.home_directory, '.a.txt')
        lib.touch(self.home_directory, '.b.txt')
        with cd(self.home_directory):
            os.symlink('.a.txt', '.link-a.txt')
            os.symlink('.b.txt', '.link-b-1.txt')
            os.symlink('.b.txt', '.link-b-2.txt')
            assert os.path.exists('.link-a.txt')
            assert os.path.exists('.link-b-1.txt')
            assert os.path.exists('.link-b-2.txt')
            lib.remove(self.home_directory, '.b.txt')
            symlink.cleanup_symlinks(self.home_directory)
            assert os.path.exists('.link-a.txt')
            assert not os.path.exists('.link-b-1.txt')
            assert not os.path.exists('.link-b-2.txt')

    def test_cleanup_symlinks_ignores_non_dotfiles(self):
        # TODO: Implement me!
        pass
