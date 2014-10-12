import os
import shutil

# pylint: disable=invalid-name
class cd(object):
    "Use with the `with` keyword to change directory."""
    def __init__(self, pathname):
        self.pathname = pathname
        self.saved_pathname = None

    def __enter__(self):
        self.saved_pathname = os.getcwd()
        os.chdir(self.pathname)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_pathname)

def create_symlinks(config):
    """Symlinks files from the dotfiles directory to the home directory.

    Args:
        config: A Config object that contains the dotfiles directory.
    """
    source_directory = config.directory
    target_directory = os.getenv('HOME')
    if not os.path.isdir(source_directory):
        print 'dotfiles directory not found: %s' % source_directory
        return
    print 'symlinking files from %s' % source_directory
    with cd(source_directory):
        excludes = set(config.excludes)
        for pathname in os.listdir('.'):
            basename = os.path.basename(pathname)
            if basename in excludes:
                continue
            source = os.path.join(source_directory, basename)
            target = os.path.join(target_directory, basename)
            if os.path.islink(target):
                os.unlink(target)
            if os.path.isfile(target):
                os.remove(target)
            if os.path.isdir(target):
                shutil.rmtree(target)
            os.symlink(source, target)
            print 'symlinked %s' % target

def cleanup_symlinks(directory):
    """Removes broken symlinks from a directory.

    Args:
        directory: The directory to look for broken symlinks.
    """
    for pathname in os.listdir(directory):
        pathname = os.path.join(directory, pathname)
        if not os.path.islink(pathname):
            continue
        if os.path.exists(os.readlink(pathname)):
            continue
        print 'removing broken link: %s' % pathname
        os.unlink(pathname)

