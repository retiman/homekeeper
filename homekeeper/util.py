import os
import subprocess

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

# pylint: disable=invalid-name
def sh(command):
    """Prints a command executes it.

    Args:
        command: The command to execute.

    Returns:
        The output of the command, discarding anything printed to standard
        error.
    """
    print command
    proc = subprocess.Popen(command.split(' '),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, _ = proc.communicate()
    return out

def remove_broken_symlinks(directory):
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
        print 'removing broken link: %s' % pathname
        os.unlink(pathname)

