import homekeeper.filesystem_testcase
import homekeeper.main
import logging

from homekeeper.common import (cd, makedirs)


logging.basicConfig(format='%(message)s', level=logging.DEBUG)

class TestMain(homekeeper.filesystem_testcase.FilesystemTestCase):
    def setup_method(self):
        super(TestMain, self).setup_method()
        self.patch('homekeeper.common')
        self.patch('homekeeper.main')
        self.main = homekeeper.main.Main()

    def setup_symlink(self):
        source = self.touch(self.home('dotfiles', '.vimrc'))
        target = self.path(self.home('.vimrc'))
        return source, target

    def verify_symlink(self, source, target):
        assert self.os.path.exists(source)
        assert self.os.path.exists(target)
        assert self.os.path.islink(target)
        assert source == self.os.readlink(target)
        if self.os.path.isfile(source):
            assert self.os.path.isfile(target)
        if self.os.path.isdir(source):
            assert self.os.path.isdir(target)

    def test_symlink_with_no_target(self):
        source, target = self.setup_symlink()
        self.main.symlink(source, target)
        self.verify_symlink(source, target)

    def test_symlink_with_file_target(self):
        source, target = self.setup_symlink()
        self.touch(target)
        self.main.symlink(source, target, overwrite=True)
        self.verify_symlink(source, target)

    def test_symlink_with_directory_target(self):
        source, target = self.setup_symlink()
        makedirs(self.os.path.dirname(target))
        self.main.symlink(source, target, overwrite=True)
        self.verify_symlink(source, target)

    def test_symlink_with_symlink_target(self):
        source, target = self.setup_symlink()
        original_source = self.touch(self.home('vimrc'))
        self.os.symlink(original_source, target)
        self.main.symlink(source, target, overwrite=True)
        self.verify_symlink(source, target)

    def test_symlink_with_no_overwrite(self):
        source, target = self.setup_symlink()
        self.touch(target)
        self.main.symlink(source, target, overwrite=False)
        assert self.os.path.exists(source)
        assert self.os.path.exists(target)
        assert not self.os.path.islink(target)

    def test_restore_symlink(self):
        source, target = self.setup_symlink()
        self.main.symlink(source, target, overwrite=True)
        self.main.restore(source, target, overwrite=True)
        assert not self.os.path.islink(target)

    def test_restore_symlink_with_no_target(self):
        source, target = self.setup_symlink()
        self.main.symlink(source, target, overwrite=True)
        self.os.unlink(target)
        self.main.restore(source, target, overwrite=False)
        assert not self.os.path.exists(target)

    def test_create_symlinks(self):
        source, target = self.setup_symlink()
        source_directory = self.os.path.dirname(source)
        assert self.os.path.exists(source)
        assert not self.os.path.exists(target)
        self.main.create_symlinks(source_directory, self.home(), overwrite=True)
        self.verify_symlink(source, target)

    def test_create_symlinks_with_no_source_directory(self):
        self.os.makedirs(self.home())
        assert self.os.path.exists(self.home())
        assert not self.os.path.exists(self.home('dotfiles'))
        self.main.create_symlinks(self.home('dotfiles'), self.home(),
                                  overwrite=True)
        assert self.os.listdir(self.home()) == []

    def test_create_symlinks_with_no_overwrite(self):
        source, target = self.setup_symlink()
        source_directory = self.os.path.dirname(source)
        self.touch(target)
        self.main.create_symlinks(source_directory, self.home(),
                                  overwrite=False)
        assert self.os.path.exists(source)
        assert self.os.path.exists(target)
        assert not self.os.path.islink(target)

    def test_create_symlinks_with_multiple_sources(self):
        source_files = ['.bash_profile', '.gitignore', '.gvimrc', '.vimrc', ]
        source_directories = ['bin', '.git', '.vim']
        excludes = ['.git', '.gitignore']
        for pathname in source_files:
            self.touch(self.home('dotfiles', pathname))
            self.touch(self.home(pathname))
        for pathname in source_directories:
            makedirs(self.home('dotfiles', pathname))
            self.touch(self.home(pathname))
        self.main.create_symlinks(self.home('dotfiles'), self.home(),
                                  excludes=excludes, overwrite=True)
        for pathname in source_files:
            if pathname in excludes:
                assert not self.os.path.islink(self.home(pathname))
            else:
                self.verify_symlink(self.home('dotfiles', pathname),
                                    self.home(pathname))

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
