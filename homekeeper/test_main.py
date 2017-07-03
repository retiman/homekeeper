import homekeeper.filesystem_testcase
import homekeeper.main

from homekeeper.common import (cd, makedirs)


class TestMain(homekeeper.filesystem_testcase.FilesystemTestCase):
    def setup_method(self):
        super(TestMain, self).setup_method()
        self.patch('homekeeper.common')
        self.patch('homekeeper.main')
        self.main = homekeeper.main.Main()

    def setup_symlink(self):
        source = self.touch(self.path(self.home(), 'dotfiles', '.vimrc'))
        target = self.path(self.home(), '.vimrc')
        return source, target

    def verify_symlink(self, source, target):
        assert self.os.path.islink(target)
        assert source == self.os.readlink(target)

    def test_symlink_with_no_target(self):
        source, target = self.setup_symlink()
        self.main.symlink(source, target)
        self.verify_symlink(source, target)

    def test_symlink_with_file_target(self):
        source, target = self.setup_symlink()
        self.touch(target)
        self.main.symlink(source, target)
        self.verify_symlink(source, target)

    def test_symlink_with_directory_target(self):
        source, target = self.setup_symlink()
        makedirs(self.os.path.dirname(target))
        self.main.symlink(source, target)
        self.verify_symlink(source, target)

    def test_symlink_with_symlink_target(self):
        source, target = self.setup_symlink()
        original_source = self.touch(self.path(self.home(), 'vimrc'))
        self.os.symlink(original_source, target)
        self.main.symlink(source, target)
        self.verify_symlink(source, target)

    def test_cleanup_symlinks(self):
        self.touch('existing.txt')
        self.os.symlink('existing.txt', 'existing-link.txt')
        self.os.symlink('non-existing-1.txt', 'non-existing-1-link.txt')
        self.os.symlink('non-existing-2.txt', 'non-existing-2-link.txt')
        self.main.cleanup_symlinks('/')
        assert self.os.path.exists('existing.txt')
        assert self.os.path.exists('existing-link.txt')
        assert not self.os.path.exists('non-existing-1-link.txt')
        assert not self.os.path.exists('non-existing-2-link.txt')
