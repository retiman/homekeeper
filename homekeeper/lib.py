import errno
import logging
import os
import shutil
import homekeeper.exceptions


HomekeeperException = homekeeper.exceptions.HomekeeperException


class cd:
    def __init__(self, pathname):
        self.pathname = pathname
        self.saved_pathname = None

    def __enter__(self):
        self.saved_pathname = os.getcwd()
        logging.debug("changing directory: %s", self.pathname)
        os.chdir(self.pathname)

    def __exit__(self, etype, value, traceback):
        logging.debug("changing directory: %s", self.saved_pathname)
        os.chdir(self.saved_pathname)


def fopen(*args, **kwargs):
    return open(*args, **kwargs)


def get_current_working_directory():
    return os.path.realpath(os.getcwd())


def get_home_directory():
    return os.getenv('HOME')


def makedirs(*args):
    try:
        directory = os.path.join(*args)
        logging.debug("making directory: %s", directory)
        os.makedirs(directory)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(directory):
            pass
        else:
            raise


def remove(*args):
    try:
        target = os.path.join(*args)
        if os.path.islink(target):
            os.unlink(target)
            logging.debug("removed symlink: %s", target)
            return
        if os.path.isfile(target):
            os.remove(target)
            logging.debug("removed file: %s", target)
            return
        if os.path.isdir(target):
            shutil.rmtree(target)
            logging.debug("removed directory: %s", target)
            return
    except IOError:
        logging.debug("could not remove path: %s", target)


def touch(*args):
    target = os.path.join(*args)
    makedirs(os.path.dirname(target))
    with fopen(target, 'a', encoding='utf-8'):
        logging.debug("touching path: %s", target)
        os.utime(target)


def process_directories(source_directory, target_directory, config_data=None, overwrite=True, process=None):
    if config_data is None:
        raise HomekeeperException('no value set for config_data')
    if not process:
        raise HomekeeperException('no value set for process')
    if not os.path.isdir(source_directory):
        logging.info("dotfiles directory not found: %s", source_directory)
        return
    if source_directory == target_directory:
        logging.error("source and target directory are the same: %s", source_directory)
        return
    logging.info("processing paths in directory: %s", source_directory)
    with cd(source_directory):
        logging.debug("excluding paths: %s", config_data.excludes)
        for pathname in os.listdir('.'):
            basename = os.path.basename(pathname)
            source = os.path.join(source_directory, basename)
            target = os.path.join(target_directory, basename)
            if basename in config_data.excludes:
                logging.debug("skipping because path is excluded: %s", basename)
                continue
            logging.debug("processing %s -> %s", source, target)
            process(source, target, overwrite=overwrite)
