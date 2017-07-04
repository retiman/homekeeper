import errno
import os


class cd(object):
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
    directory = dirname or '/'
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(directory):
            pass
        else:
            raise
