import fake_filesystem
import homekeeper
import homekeeper.config
import homekeeper.util
import __builtin__

def create_fake_filesystem():
    """Create a fake filesystem and and use it in all modules.

    Returns:
        The created fake filesystem object and os module.
    """
    filesystem = fake_filesystem.FakeFilesystem()
    # pylint: disable=invalid-name
    os = fake_filesystem.FakeOsModule(filesystem)
    os.getenv = _getenv
    _replace_modules(os)
    _replace_builtins(filesystem)
    return [filesystem, os]

def _replace_builtins(filesystem):
    """Replaces Python builtins."""
    __builtin__.open = fake_filesystem.FakeFileOpen(filesystem)

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
