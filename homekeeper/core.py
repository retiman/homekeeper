import homekeeper.common
import logging
import os
import shutil

cd = homekeeper.common.cd
makedirs = homekeeper.common.makedirs


def symlink(config, source, target):
    """Removes a target symlink/file/directory before replacing it with
    symlink. Also creates the parent directory if it does not exist.

    Args:
        config: Homekeeper configuration.
        source: Original source of the symlink.
        target: Path of symlink target, can be file or directory.
    """
    dirname = os.path.dirname(target)
    if not os.path.exists(dirname):
        makedirs(dirname)
    if source == target:
        logging.debug('skipping %s; source and target are the same', source)
        return
    if os.path.exists(target) and not config.overwrite:
        logging.debug('skipping %s; will not overwrite', target)
        return
    remove(target)
    os.symlink(source, target)
    logging.info('symlinked %s -> %s', source, target)


def restore(config, source, target):
    """Restores a symlink to its target. Afterwards, the target will no
    longer be a symlink.

    Args:
        config: Homekeeper configuration.
        source: Original source of the symlink.
        target: Path of symlink target, can be file or directory.
    """
    if source == target:
        logging.debug('skipping %s; source and target are the same', source)
        return
    if not config.overwrite:
        if not os.path.exists(target):
            logging.debug('skipping %s; missing link target', target)
            return
        if not os.path.islink(target):
            logging.debug('skipping %s; resource is not a link', target)
            return
        if os.readlink(target) != source:
            logging.debug('skipping %s; symlink target is wrong', target)
            return
    remove(target)
    if os.path.isfile(source):
        shutil.copy(source, target)
        logging.debug('restored file %s -> %s', source, target)
    elif os.path.isdir(source):
        shutil.copytree(source, target, symlinks=True)
        logging.debug('restored directory %s -> %s', source, target)
    else:
        logging.info('skipping %s; not a file or directory', target)


def create_symlinks(config, source_directory, target_directory):
    """Symlinks files from the source directory to the target directory.

    For example, suppose that your `source_directory` is your dotfiles
    directory and contains a file named '.vimrc'.  If the `target_directory`
    is your home directory, then this is the result:

        $HOME/.vimrc -> $HOME/dotfiles/.vimrc

    The existing $HOME/.vimrc will be removed.

    Args:
        config: Homekeeper configuration.
        source_directory: The source directory where your dotfiles are.
        target_directory: The target directory for symlinking.
    """
    process_directories(config, source_directory, target_directory, symlink)


def create_symlinks_from_base(config):
    if not config.override:
        return
    create_symlinks(config, config.base_directory, config.home)


def create_symlinks_from_dotfiles(config):
    create_symlinks(config, config.dotfiles_directory, config.home)


def restore_symlinks(config, source_directory, target_directory):
    """Realizes the symlinks files in the source directory that have been
    symlinked to the target directory.

    For example, suppose your home directory contains:

        $HOME/.vimrc -> $HOME/dotfiles/.vimrc

    Then the result will be:

        $HOME/.vimrc

    The $HOME/.vimrc file will contain to contains of $HOME/dotfiles/.vimrc.
    Any symlinks in the source directory that do not point to the target
    directory will not be restored.

    Args:
        config: Homekeeper configuration.
        source_directory: The source directory where your dotfiles are.
        target_directory: The target directory for symlinking.
    """
    process_directories(config, source_directory, target_directory, restore)


def restore_symlinks_from_base(config):
    if not config.override:
        return
    restore_symlinks(config, config.base_directory, config.home)


def restore_symlinks_from_dotfiles(config):
    restore_symlinks(config, config.dotfiles_directory, config.home)


def cleanup_symlinks(directory):
    """Removes broken symlinks from a directory.

    Args:
        directory: The directory to look for broken symlinks.
    """
    logging.info('removing broken symlinks in %s', directory)
    for item in os.listdir(directory):
        pathname = os.path.join(directory, item)
        if not os.path.islink(pathname):
            logging.debug('skipping %s; not a symlink', pathname)
            continue
        if os.path.exists(os.readlink(pathname)):
            logging.debug('skipping %s; not a broken symlink', pathname)
            continue
        logging.info('removing broken link: %s', pathname)
        os.unlink(pathname)
    logging.info('finished removing symlinks in %s', directory)


def remove(target):
    if os.path.islink(target):
        os.unlink(target)
        logging.debug('removed symlink %s', target)
    if os.path.isfile(target):
        os.remove(target)
        logging.debug('removed file %s', target)
    if os.path.isdir(target):
        shutil.rmtree(target)
        logging.debug('removed directory %s', target)


def process_directories(config, source_directory, target_directory, process):
    if not os.path.isdir(source_directory):
        logging.info('dotfiles directory not found: %s', source_directory)
        return
    if source_directory == target_directory:
        logging.error('source and target directory are the same')
        return
    logging.info('processing files in %s', source_directory)
    with cd(source_directory):
        for pathname in os.listdir('.'):
            basename = os.path.basename(pathname)
            source = os.path.join(source_directory, basename)
            target = os.path.join(target_directory, basename)
            if basename in config.excludes:
                logging.debug('skipping %s; resource is excluded', basename)
                continue
            process(config, source, target)
