import logging
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

def create_symlinks(source_directory, target_directory, excludes=None,
                    includes=None):
    """Symlinks files from the dotfiles directory to the home directory.

    Args:
        source_directory: The source directory where your dotfiles are.
        target_directory: The target directory for symlinking.
        excludes: An array of files excluded from symlinking.
        includes: An array of paths in which only the basename gets symlinked
    """
    excludes = excludes if excludes is not None else []
    includes = includes if includes is not None else []
    if not os.path.isdir(source_directory):
        logging.info('dotfiles directory not found: %s', source_directory)
        return
    logging.info('symlinking files from %s', source_directory)
    with cd(source_directory):
        excludes = set(excludes)
        includes = set(includes)
        for pathname in os.listdir('.'):
            basename = os.path.basename(pathname)
            if basename in excludes:
                logging.debug('Skipping excluded resource: %s', basename)
                continue
            # Our source and target are set, unless basename matches something
            # within our include path, then basename becomes include.
            for include in includes:
                if os.path.commonprefix([basename, include]):
                    basename = include
            source = os.path.join(source_directory, basename)
            target = os.path.join(target_directory, basename)
            cleanup_target(target)
            os.symlink(source, target)
            logging.info('symlinked %s -> %s', target, source)

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
        logging.info('removing broken link: %s', pathname)
        os.unlink(pathname)

def cleanup_target(target):
    """Removes a target symlink/file/directory before replacing it with symlink.

    Args:
        target: Path of symlink target, can be file or directory.
    """
    if os.path.islink(target):
        os.unlink(target)
        logging.debug('removed symlink %s', target)
    if os.path.isfile(target):
        os.remove(target)
        logging.debug('removed file %s', target)
    if os.path.isdir(target):
        shutil.rmtree(target)
        logging.debug('removed directory %s', target)

