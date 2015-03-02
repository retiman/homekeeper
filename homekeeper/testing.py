import fake_filesystem
import homekeeper
import homekeeper.config
import homekeeper.util
import __builtin__

def init():
    """Create a fake filesystem and and use it in all modules.

    Returns:
        The created fake filesystem object and os module.
    """
    fake_fs = fake_filesystem.FakeFilesystem()
    fake_os = fake_filesystem.FakeOsModule(fake_fs)
    fake_os.getenv = _getenv
    _replace_modules(fake_os)
    _replace_builtins(fake_fs)
    return (fake_fs, fake_os)

def _replace_builtins(fake_fs):
    """Replaces Python builtins."""
    __builtin__.open = fake_filesystem.FakeFileOpen(fake_fs)

def _replace_modules(fake_os):
    """Replaces filesystem modules and functions with fakes."""
    homekeeper.os = fake_os
    homekeeper.config.os = fake_os
    homekeeper.util.os = fake_os
    homekeeper.util.shutil.move = fake_os.rename
    homekeeper.util.shutil.rmtree = fake_os.rmdir

def _getenv(key):
    return {
        'HOME': '/home/johndoe'
    }[key]
