import logging
import mock
import pyfakefs
import pytest
import click.testing
import homekeeper.cli
import homekeeper.config
import homekeeper.lib


config = homekeeper.config
lib = homekeeper.lib
CliRunner = click.testing.CliRunner
ConfigData = homekeeper.config.ConfigData


class BaseFakeFilesystemTest:
    """A base test class for interacting with a fake filesystem.  Working with a real filesystem is possible; however,
    two problems need to be resolved:

    1) The build will fail on Windows; a Linux subsystem for Windows must be installed as a workaround.
    2) Resolving os.getenv('HOME') will be problematic; all calls must be patched to return a tmpdir path.
    """
    def setup_method(self):
        self.fake_fs = pyfakefs.fake_filesystem.FakeFilesystem()
        self.fake_fopen = pyfakefs.fake_filesystem.FakeFileOpen(self.fake_fs)
        self.fake_os = pyfakefs.fake_filesystem.FakeOsModule(self.fake_fs)
        self.fake_shutil = pyfakefs.fake_filesystem_shutil.FakeShutilModule(self.fake_fs)
        self.home_directory = None
        self.dotfiles_directory = None
        self.directories = []
        self.files = []
        self.patchers = []
        self.setup_patchers()
        self.setup_fs(self.fake_os)

    def setup_patchers(self):
        logging.info('patching homekeeper')
        self.patchers.append(mock.patch('homekeeper.config.fopen', self.fake_fopen))
        self.patchers.append(mock.patch('homekeeper.config.os', self.fake_os))
        self.patchers.append(mock.patch('homekeeper.lib.fopen', self.fake_fopen))
        self.patchers.append(mock.patch('homekeeper.lib.os', self.fake_os))
        self.patchers.append(mock.patch('homekeeper.lib.shutil', self.fake_shutil))
        self.patchers.append(mock.patch('homekeeper.symlink.os', self.fake_os))
        self.patchers.append(mock.patch('homekeeper.symlink.shutil', self.fake_shutil))
        # Note that only `shutildisk_usage()` is faked, according to fake_filesystem_shutil.py.  The rest of the
        # functions will work only if `os` and `open` are patched as well.
        logging.info('patching shutil')
        self.patchers.append(mock.patch('shutil.open', self.fake_fopen))
        self.patchers.append(mock.patch('shutil.os', self.fake_os))
        for patcher in self.patchers:
            patcher.start()

    def setup_fs(self, os):
        self.home_directory = os.path.join(os.sep, 'home', 'johndoe')
        self.dotfiles_directory = os.path.join(self.home_directory, 'dotfiles')
        self.directories = [
            self.home_directory,
            self.dotfiles_directory,
            os.path.join(self.dotfiles_directory, '.vim')
        ]
        self.files = [
            os.path.join(self.dotfiles_directory, '.bashrc'),
            os.path.join(self.dotfiles_directory, '.vimrc'),
        ]
        logging.info("setting HOME environment variable in fake os: %s", self.home_directory)
        os.environ['HOME'] = str(self.home_directory)
        logging.info("setting up directories in fake fs: %s", self.directories)
        for directory in self.directories:
            lib.makedirs(directory)
        logging.info("setting up files in fake fs: %s", self.files)
        for file in self.files:
            lib.touch(file)

    def setup_file_symlink(self, filename):
        os = self.fake_os
        source = os.path.join(self.dotfiles_directory, filename)
        target = os.path.join(self.home_directory, filename)
        lib.touch(source)
        lib.remove(target)
        os.symlink(source, target)
        return source, target

    def setup_directory_symlink(self, dirname):
        os = self.fake_os
        source = os.path.join(self.dotfiles_directory, dirname)
        target = os.path.join(self.home_directory, dirname)
        lib.makedirs(source)
        lib.remove(target)
        os.symlink(source, target)
        return source, target

    def teardown_method(self):
        for patcher in self.patchers:
            patcher.stop()
        del self.fake_fs

    @pytest.fixture
    def fopen(self):
        return self.fake_fopen

    @pytest.fixture
    def os(self):
        return self.fake_os

    @pytest.fixture
    def shutil(self):
        return self.fake_shutil

    @pytest.fixture
    def files(self):
        files = [
            '.bashrc',
            '.bash_profile',
            '.gitconfig',
            '.gitignore',
            '.vimrc',
        ]
        for filename in files:
            lib.touch(self.dotfiles_directory, filename)
        return files

    @pytest.fixture
    def directories(self):
        directories = [
            'bin',
            '.i3',
            '.vim',
        ]
        for dirname in directories:
            lib.makedirs(self.dotfiles_directory, dirname)
        return directories


class BaseCliTest(BaseFakeFilesystemTest):
    def setup_method(self):
        super().setup_method()
        os = self.fake_os
        self.runner = CliRunner()
        self.config_data = ConfigData()
        self.config_data.directories = [os.path.join(self.dotfiles_directory)]

    def run(self, *args):
        result = self.runner.invoke(homekeeper.cli.main, args)
        logging.info("stdout: %s", result.stdout)
        return result
