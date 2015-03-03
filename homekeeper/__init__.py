#!/usr/bin/env python2
"""This program helps organize and version your dot files with Git."""
import homekeeper.config
import homekeeper.util
import logging
import os
import shutil

__version__ = '3.1.0'

class Homekeeper(object):
    """Organizes and versions your dot files."""

    def __init__(self, pathname=None):
        self.pathname = homekeeper.config.Config.PATHNAME
        if pathname is not None:
            self.pathname = pathname
        self.config = homekeeper.config.Config(self.pathname)

    def init(self):
        """Writes a configuration file with cwd as the dotfiles directory.

        Configuration file is written as JSON, and will be removed if it exists
        already.  If configuration already exists, the new dotfiles directory
        path will be merged into existing configuration.
        """
        self.config.directory = os.path.realpath(os.getcwd())
        logging.info('setting dotfiles directory to %s', self.config.directory)
        self.config.save()

    def track(self, pathname):
        """Moves a file or directory into your dotfiles directory so it can be
        symlinked later.

        Args:
            pathname: The pathname of the directory or file you want to track.
        """
        if not os.path.exists(pathname):
            logging.info("pathname not found; won't track %s", pathname)
            return
        basename = os.path.basename(pathname)
        target = os.path.join(self.config.directory, basename)
        if os.path.exists(target):
            logging.info('this path is already tracked at %s', target)
            return
        shutil.move(pathname, target)
        logging.info('moved %s to %s', pathname, target)
        os.symlink(target, pathname)
        logging.info('symlinked %s -> %s', pathname, target)

    def link(self):
        """Symlinks all files and directories from your dotfiles directory into
        your home directory.
        """
        home = os.getenv('HOME')
        if self.config.override:
            homekeeper.util.create_symlinks(self.config.base,
                                            home,
                                            excludes=self.config.excludes,
                                            includes=self.config.includes)
        homekeeper.util.create_symlinks(self.config.directory,
                                        home,
                                        excludes=self.config.excludes,
                                        includes=self.config.includes)
        homekeeper.util.cleanup_symlinks(home)

