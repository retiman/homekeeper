import homekeeper.test_case
import logging

from homekeeper.common import makedirs
from homekeeper import core

os = None


class TestCore(homekeeper.test_case.TestCase):
    def setup_method(self):
        super(TestCore, self).setup_method()
        self.setup_filesystem()
        self.patch('homekeeper.common')
        self.patch('homekeeper.core')

    def setup_filesystem(self):
        global os
        os = self.os

    def setup_symlink(self):
        source = self.setup_file(self.home(), 'dotfiles', '.vimrc')
        target = os.path.join(self.home(), '.vimrc')
        return source, target

    def verify_symlink(self, source, target):
        assert os.path.exists(source)
        assert os.path.exists(target)
        assert os.path.islink(target)
        assert source == os.readlink(target)
        if os.path.isfile(source):
            assert os.path.isfile(target)
        if os.path.isdir(source):
            assert os.path.isdir(target)

    def test_symlink_with_no_target(self):
        source, target = self.setup_symlink()
        core.symlink(source, target)
        self.verify_symlink(source, target)

    def test_symlink_with_file_target(self):
        source, target = self.setup_symlink()
        self.setup_file(target)
        core.symlink(source, target, overwrite=True)
        self.verify_symlink(source, target)

    def test_symlink_with_directory_target(self):
        source, target = self.setup_symlink()
        makedirs(os.path.dirname(target))
        core.symlink(source, target, overwrite=True)
        self.verify_symlink(source, target)

    def test_symlink_with_symlink_target(self):
        source, target = self.setup_symlink()
        original_source = self.setup_file(self.home(), 'vimrc')
        os.symlink(original_source, target)
        core.symlink(source, target, overwrite=True)
        self.verify_symlink(source, target)

    def test_symlink_with_no_overwrite(self):
        source, target = self.setup_symlink()
        self.setup_file(target)
        core.symlink(source, target, overwrite=False)
        assert os.path.exists(source)
        assert os.path.exists(target)
        assert not os.path.islink(target)

    def test_restore_file_symlink(self):
        source, target = self.setup_symlink()
        core.symlink(source, target, overwrite=True)
        core.restore(source, target, overwrite=True)
        assert not os.path.islink(target)
        assert os.path.isfile(target)

    def test_restore_directory_symlink(self):
        source = self.home('dotfiles', '.vim')
        target = self.home('.vim')
        self.setup_file(source, '.vim', 'autoload', 'pathogen.vim')
        core.symlink(source, target, overwrite=True)
        core.restore(source, target, overwrite=True)
        assert not os.path.islink(target)
        assert os.path.isdir(target)
        assert os.path.isfile(self.path(target, '.vim', 'autoload',
                              'pathogen.vim'))

    def test_restore_symlink_with_no_target(self):
        source, target = self.setup_symlink()
        core.symlink(source, target, overwrite=True)
        os.unlink(target)
        core.restore(source, target, overwrite=False)
        assert not os.path.exists(target)

    def test_create_symlinks(self):
        source, target = self.setup_symlink()
        source_directory = os.path.dirname(source)
        assert os.path.exists(source)
        assert not os.path.exists(target)
        core.create_symlinks(source_directory, self.home(), overwrite=True)
        self.verify_symlink(source, target)

    def test_create_symlinks_with_no_source_directory(self):
        makedirs(self.home())
        assert os.path.exists(self.home())
        assert not os.path.exists(self.home('dotfiles'))
        core.create_symlinks(self.home('dotfiles'), self.home(), overwrite=True)
        assert os.listdir(self.home()) == []

    def test_create_symlinks_with_no_overwrite(self):
        source, target = self.setup_symlink()
        source_directory = os.path.dirname(source)
        self.setup_file(target)
        core.create_symlinks(source_directory, self.home(),
                                  overwrite=False)
        assert os.path.exists(source)
        assert os.path.exists(target)
        assert not os.path.islink(target)

    def test_create_symlinks_with_multiple_sources(self):
        source_files = ['.bash_profile', '.gitignore', '.gvimrc', '.vimrc']
        source_directories = ['bin', '.git', '.vim']
        excludes = ['.git', '.gitignore']
        for item in source_files:
            self.setup_file(self.home(), 'dotfiles', item)
            self.setup_file(self.home(), item)
        for item in source_directories:
            self.setup_directory(self.home(), 'dotfiles', item)
            self.setup_file(self.home(), item)
        core.create_symlinks(self.home('dotfiles'), self.home(),
                             excludes=excludes, overwrite=True)
        for item in source_files:
            if item in excludes:
                assert not os.path.islink(self.home(item))
            else:
                self.verify_symlink(self.home('dotfiles', item),
                                    self.home(item))

    def test_cleanup_symlinks(self):
        self.setup_file('existing.txt')
        os.symlink('existing.txt', 'existing-link.txt')
        os.symlink('non-existing-1.txt', 'non-existing-1-link.txt')
        os.symlink('non-existing-2.txt', 'non-existing-2-link.txt')
        core.cleanup_symlinks('/')
        assert os.path.exists('existing.txt')
        assert os.path.exists('existing-link.txt')
        assert not os.path.exists('non-existing-1-link.txt')
        assert not os.path.exists('non-existing-2-link.txt')
