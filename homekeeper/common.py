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


def makedirs(pathname):
    try:
        os.makedirs(pathname)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(pathname):
            pass
        else:
            raise
