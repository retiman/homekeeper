import logging
import os
import shutil

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

# pylint: disable=unused-argument
def restore(source_directory, target_directory, excludes=None,
            cherrypicks=None):
    """Restores symlinks from the source directory to the target directory.

    For example, suppose that there is a symlink:

        $HOME/.vimrc -> $HOME/dotfiles/.vimrc

    You want to undo this symlink so that the actual file in
    $HOME/dotfiles/.vimrc is copied to $HOME/.vimrc and the symlink is undone.
    In this case, the source_directory is $HOME/dotfiles and the target
    directory is $HOME.
    """
    assert not isinstance(excludes, basestring)
    assert not isinstance(cherrypicks, basestring)
    excludes = frozenset(excludes or [])
    cherrypicks = frozenset(cherrypicks or [])
    if not os.path.isdir(source_directory):
        logging.info('dotfiles directory not found: %s', source_directory)
        return
    logging.info('restoring files from %s', source_directory)
    # Restore the manually included files from the include directive; these will
    # never be excluded.
    with cd(source_directory):
        for pathname in cherrypicks:
            source = os.path.join(source_directory, pathname)
            target = os.path.join(target_directory, pathname)
            if os.path.exists(source) and os.path.islink(target):
                prepare_target(target)
                shutil.copy(source, target)
                logging.info('restored %s', target)
            else:
                # This is a harmless condition that can occur if you've included
                # a file from your base directory (and it is present), but it is
                # not present from your dotfiles directory.
                logging.debug('skipping missing resource: %s', source)
    # Restore the rest of the files, excluding any from the exclude directive.
    with cd(source_directory):
        included = frozenset(map(firstdir, cherrypicks))
        for pathname in os.listdir('.'):
            basename = os.path.basename(pathname)
            source = os.path.join(source_directory, basename)
            target = os.path.join(target_directory, basename)
            # Skip any excluded paths.
            if basename in excludes:
                logging.debug('skipping excluded resource: %s', basename)
                continue
            # Skip any included paths that were already symlinked earlier.
            if os.path.isdir(basename) and basename in included:
                logging.debug('skipping already restored resource: %s',
                              basename)
                continue
            # Skip any paths whose targets don't seem to be symlinks.
            if not os.path.islink(target):
                logging.debug('skipping non linked resource: %s', basename)
                continue
            prepare_target(target)
            if os.path.isfile(source):
                shutil.copy(source, target)
            elif os.path.isdir(source):
                shutil.copytree(source, target)
            else:
                logging.warning('skipping invalid resource: %s', source)
                continue
            logging.info('restored %s', target)

def create_symlinks(source_directory, target_directory, excludes=None,
                    cherrypicks=None):
    """Symlinks files from the dotfiles directory to the home directory.

    Args:
        source_directory: The source directory where your dotfiles are.
        target_directory: The target directory for symlinking.
        excludes: An array of paths excluded from symlinking.
        cherrypicks: An array of paths in which only the base gets symlinked.
    """
    assert not isinstance(excludes, basestring)
    assert not isinstance(cherrypicks, basestring)
    excludes = frozenset(excludes or [])
    cherrypicks = frozenset(cherrypicks or [])
    if not os.path.isdir(source_directory):
        logging.info('dotfiles directory not found: %s', source_directory)
        return
    logging.info('symlinking files from %s', source_directory)
    # Symlink the manually included files from the include directive; these will
    # never be excluded.
    with cd(source_directory):
        for pathname in cherrypicks:
            source = os.path.join(source_directory, pathname)
            target = os.path.join(target_directory, pathname)
            if os.path.exists(source):
                prepare_target(target)
                os.symlink(source, target)
                logging.info('symlinked %s -> %s', target, source)
            else:
                # This is a harmless condition that can occur if you've included
                # a file from your base directory (and it is present), but it is
                # not present from your dotfiles directory.
                logging.debug('skipping missing resource: %s', source)
    # Symlink the rest of the files, excluding any from the exclude directive.
    with cd(source_directory):
        included = frozenset(map(firstdir, cherrypicks))
        for pathname in os.listdir('.'):
            basename = os.path.basename(pathname)
            source = os.path.join(source_directory, basename)
            target = os.path.join(target_directory, basename)
            # Skip any excluded paths.
            if basename in excludes:
                logging.debug('skipping excluded resource: %s', basename)
                continue
            # Skip any included paths that were already symlinked earlier.
            if os.path.isdir(basename) and basename in included:
                logging.debug('skipping already symlinked resource: %s',
                              basename)
                continue
            prepare_target(target)
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

def prepare_target(target):
    """Removes a target symlink/file/directory before replacing it with symlink.
    Also creates the parent directory if it does not exist.

    Args:
        target: Path of symlink target, can be file or directory.
    """
    dirname = os.path.dirname(target)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    if os.path.islink(target):
        os.unlink(target)
        logging.debug('removed symlink %s', target)
    if os.path.isfile(target):
        os.remove(target)
        logging.debug('removed file %s', target)
    if os.path.isdir(target):
        shutil.rmtree(target)
        logging.debug('removed directory %s', target)

def fopen(*args, **kwargs):
    """Alias for __builtin__.open. This exists so tests may mock this function
    without overriding open for all modules.
    """
    return open(*args, **kwargs)

def firstdir(pathname):
    """Gets the first directory of the path.

    For example, if pathname is '/home/johndoe', this function returns '/home'.
    """
    head, tail = os.path.split(pathname)
    if not head or head is '/':
        return tail
    else:
        return firstdir(head)

