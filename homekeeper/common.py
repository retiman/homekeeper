import errno
import os


class cd(object): # pylint: disable=too-few-public-methods
    "Use with the `with` keyword to change directory."""
    def __init__(self, pathname):
        self.pathname = pathname
        self.saved_pathname = None

    def __enter__(self):
        self.saved_pathname = os.getcwd()
        os.chdir(self.pathname)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_pathname)


def fopen(*args, **kwargs):
    """Alias for __builtin__.open. This exists so tests may mock this function
    without overriding open for all modules.
    """
    return open(*args, **kwargs)


def makedirs(dirname):
    """Creates a directory safely. Does not raise an error if the directory
    exists.
    """
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(dirname):
            pass
        else:
            raise
