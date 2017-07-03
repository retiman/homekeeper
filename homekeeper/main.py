import logging
import os
import shutil

from homekeeper.common import makedirs


class Main(object):
    def symlink(self, source, target):
        """Removes a target symlink/file/directory before replacing it with
        symlink. Also creates the parent directory if it does not exist.

        Args:
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
