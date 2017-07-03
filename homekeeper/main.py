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


class Main(object):
    def symlink(self, source, target):
        """Removes a target symlink/file/directory before replacing it with
        symlink. Also creates the parent directory if it does not exist.

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
        os.symlink(source, target)
        logging.info('symlinked %s -> %s', target, source)
