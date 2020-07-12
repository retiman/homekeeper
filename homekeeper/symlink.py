import logging
import os
import shutil
import homekeeper.lib


config = homekeeper.config
lib = homekeeper.lib
ConfigData = homekeeper.config.ConfigData


def cleanup_symlinks(*args):
    directory = os.path.join(*args)
    logging.info("removing broken symlinks in directory: %s", directory)
    for item in os.listdir(directory):
        pathname = os.path.join(directory, item)
        basename = os.path.basename(pathname)
        if not os.path.islink(pathname):
            logging.debug("skipping because path is not a symlink: %s", pathname)
            continue
        if os.path.exists(os.readlink(pathname)):
            logging.debug("skipping because path is not a broken symlink: %s", pathname)
            continue
        if not basename.startswith('.'):
            logging.debug("skipping because path does not start with dot: %s", pathname)
            continue
        logging.info("removing broken link: %s", pathname)
        os.unlink(pathname)
    logging.info("finished removing symlinks in directory: %s", directory)


def create_symlink(source, target, overwrite=True):
    dirname = os.path.dirname(target)
    if not os.path.exists(dirname):
        lib.makedirs(dirname)
    if source == target:
        logging.info("skipping because source and target are the same: %s", source)
        return
    if os.path.exists(target) and not overwrite:
        logging.info("skipping because target would be overwritten: %s", target)
        return
    lib.remove(target)
    os.symlink(source, target)
    logging.info('symlinked %s -> %s', source, target)


def create_symlinks(source_directory, target_directory, config_data=ConfigData(), overwrite=True):
    lib.process_directories(
        source_directory,
        target_directory,
        overwrite=overwrite,
        config_data=config_data,
        process=create_symlink)


def restore_symlink(source, target, overwrite=None): # pylint: disable=unused-argument
    if source == target:
        logging.info("skipping because source and target are the same: %s", source)
        return
    if not os.path.islink(target):
        logging.info("skipping because target is not a symlink: %s", target)
        return
    if os.readlink(target) != source:
        logging.info("skipping because target is not symlinked to source: %s", target)
        return
    lib.remove(target)
    if os.path.isfile(source):
        shutil.copyfile(source, target)
        logging.info("restored file %s -> %s", source, target)
    elif os.path.isdir(source):
        shutil.copytree(source, target, symlinks=True)
        logging.info("restored directory %s -> %s", source, target)
    else:
        logging.info("skipping because target is not a file or directory: %s", target)


def restore_symlinks(source_directory, target_directory, config_data=ConfigData()):
    lib.process_directories(
        source_directory,
        target_directory,
        config_data=config_data,
        process=restore_symlink)
