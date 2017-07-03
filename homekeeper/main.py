import logging
import os
import shutil

from homekeeper.common import makedirs


class Main(object):
    def symlink(self, source, target):
        """Removes a target symlink/file/directory before replacing it with
        symlink. Also creates the parent directory if it does not exist.

        Args:
            source: Original source of the symlink.
            target: Path of symlink target, can be file or directory.
        """
        dirname = os.path.dirname(target)
        if not os.path.exists(dirname):
            makedirs(dirname)
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
        logging.info('symlinked %s -> %s', target, source)

    def cleanup_symlinks(self, directory):
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
