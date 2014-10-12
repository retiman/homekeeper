#!/usr/bin/env python2
"""This program helps organize and version your dot files with Git."""
import homekeeper.config
import homekeeper.util
import logging
import os
import shutil

__version__ = '3.0.0'

class Homekeeper(object):
    """Organizes and versions your dot files."""

    def __init__(self, pathname=None):
        self.config = homekeeper.config.Config(pathname)

    def init(self):
        """Writes a configuration file with cwd as the dotfiles directory.

        Configuration file is written as JSON, and will be removed if it exists
        already.  If configuration already exists, the new dotfiles directory
        path will be merged into existing configuration.
        """
        pathname = os.path.realpath(os.getcwd())
        self.config.reset()
        self.config.directory = pathname
        self.config.save()

    def track(self, pathname):
        if not os.path.exists(pathname):
            logging.info("pathname not found; won't track %s", pathname)
            return
        basename = os.path.basename(pathname)
        target = os.path.join(self.config['dotfiles_directory'], basename)
        if os.path.exists(target):
            logging.info('this path is already tracked at %s', target)
            return
        logging.info('moved %s to %s', pathname, target)
        shutil.move(pathname, target)

    def link(self):
        homekeeper.util.create_symlinks(self.config)
        homekeeper.util.cleanup_symlinks(os.getenv('HOME'))
