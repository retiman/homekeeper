import errno
import fake_filesystem
import homekeeper
import homekeeper.config
import homekeeper.util
import __builtin__

# pylint: disable=invalid-name
os = None

def init():
    """Create a fake filesystem and and use it in all modules.

    Returns:
        The created fake filesystem object and os module.
    """
    fake_fs = fake_filesystem.FakeFilesystem()
    fake_os = _create_fake_os(fake_fs)
    _replace_modules(fake_os)
    _replace_builtins(fake_fs)
    _create_test_files()
    return (fake_fs, fake_os)

def dotfiles_directory():
    """The dotfiles directory in the fake filesystem."""
    return os.path.join(os.getenv('HOME'), 'dotfiles')

def base_directory():
    """The base directory for dotfiles in the fake filesystem."""
    return os.path.join(dotfiles_directory(), 'base')

def main_directory():
    """The main directory for dotfiles in the fake filesystem."""
    return os.path.join(dotfiles_directory(), 'main')

def configuration_file():
    """The configuration file for homekeeper in the fake filesystem.

    Note that this value will differ from Config.PATHNAME because this path is
    based off of _getenv function.
    """
    return os.path.join(os.getenv('HOME'), 'homekeeper.json')

def _replace_builtins(fake_fs):
    """Replaces Python builtins."""
    __builtin__.open = fake_filesystem.FakeFileOpen(fake_fs)

def _replace_modules(fake_os):
    """Replaces filesystem modules and functions with fakes."""
    homekeeper.os = fake_os
    homekeeper.config.os = fake_os
    homekeeper.testing.os = fake_os
    homekeeper.util.os = fake_os
    homekeeper.util.shutil.move = fake_os.rename
    homekeeper.util.shutil.rmtree = fake_os.rmdir

def _makedirs(makedirs):
    """Returns a version of makedirs that does not raise an exception if the
    directory already exists."""
    def safe_makedirs(pathname):
        try:
            makedirs(pathname)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(pathname):
                pass
            else:
                raise
    return safe_makedirs

def _create_fake_os(fake_fs):
    """Creates a fake os module from a fake filesystem object."""
    fake_os = fake_filesystem.FakeOsModule(fake_fs)
    fake_os.getenv = _getenv
    fake_os.makedirs = _makedirs(fake_os.makedirs)
    return fake_os

def _create_test_files():
    """Creates test files in our fake filesystem."""
    home = os.getenv('HOME')
    os.makedirs(home)
    os.makedirs(os.path.join(home, '.foo', 'bar', 'baz'))
    os.makedirs(os.path.join(home, '.vim'))
    os.makedirs(os.path.join(home, 'bin'))
    os.makedirs(base_directory())
    os.makedirs(main_directory())
    for name in ['bundle', 'ftdetect', 'ftplugin', 'ftdetect', 'syntax']:
        os.makedirs(os.path.join(home, '.vim', name))

def _getenv(key):
    return {
        'HOME': '/home/johndoe'
    }[key]

