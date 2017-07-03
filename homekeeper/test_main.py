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

    def verify_symlink(self):
        assert self.os.path.islink(target)
        assert source == self.os.readlink(target)

    def test_symlink_with_no_target(self):
        source, target = self.setup_symlink()
        self.main.symlink(source, target)
        self.verify_symlink()

    def test_symlink_with_file_target(self):
        source, target = self.setup_symlink()
        self.touch(target)
        self.main.symlink(source, target)
        self.verify_symlink()

    def test_symlink_with_directory_target(self):
        source, target = self.setup_symlink()
        makedirs(self.os.path.dirname(target))
        self.main.symlink(source, target)
        self.verify_symlink()

    def test_symlink_with_symlink_target(self):
        source, target = self.setup_symlink()
        original_source = self.touch(self.path(self.home(), 'vimrc'))
        self.os.symlink(target)
        self.main.symlink(source, target)
        self.verify_symlink()
