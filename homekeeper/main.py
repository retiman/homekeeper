import logging
import os
import shutil

from homekeeper.common import (cd, makedirs)


class Main(object):
    def symlink(self, source, target, overwrite=True):
        """Removes a target symlink/file/directory before replacing it with
        symlink. Also creates the parent directory if it does not exist.

        Args:
            source: Original source of the symlink.
            target: Path of symlink target, can be file or directory.
        """
        dirname = os.path.dirname(target)
        if not os.path.exists(dirname):
            makedirs(dirname)
        if os.path.exists(target) and not overwrite:
            logging.warn('will not overwrite; skipping %s', target)
            return
        if os.path.islink(target):
            os.unlink(target)
            logging.debug('removed symlink %s', target)
        if os.path.isfile(target):
            os.remove(target)
            logging.debug('removed file %s', target)
        if os.path.isdir(target):
            shutil.rmtree(target)
            logging.debug('removed directory %s', target)
        os.symlink(source, target)
        logging.info('symlinked %s -> %s', source, target)

    def create_symlinks(self, source_directory, target_directory,
                        excludes=set(), overwrite=True):
        """Symlinks files from the source directory to the target directory.

        For example, suppose that your `source_directory` is your dotfiles
        directory and contains a file named '.vimrc'.  If the `target_directory`
        is your home directory, then this is the result:

            $HOME/.vimrc -> $HOME/dotfiles/.vimrc

        The existing $HOME/.vimrc will be removed.

        Args:
            source_directory: The source directory where your dotfiles are.
            target_directory: The target directory for symlinking.
            excludes: An array of paths excluded from symlinking.
            ovewrite: Overwrite existing files.
        """
        if not os.path.isdir(source_directory):
            logging.info('dotfiles directory not found: %s', source_directory)
            return
        logging.info('symlinking files from %s', source_directory)
        with cd(source_directory):
            for pathname in os.listdir('.'):
                logging.debug('examining %s', pathname)
                basename = os.path.basename(pathname)
                source = os.path.join(source_directory, basename)
                target = os.path.join(target_directory, basename)
                if basename in excludes:
                    logging.debug('skipping excluded resource: %s', basename)
                    continue
                self.symlink(source, target, overwrite=overwrite)

    def cleanup_symlinks(self, directory):
        """Removes broken symlinks from a directory.

        Args:
            directory: The directory to look for broken symlinks.
        """
        for item in os.listdir(directory):
            pathname = os.path.join(directory, item)
            if not os.path.islink(pathname):
                continue
            if os.path.exists(os.readlink(pathname)):
                continue
            logging.info('removing broken link: %s', pathname)
            os.unlink(pathname)
