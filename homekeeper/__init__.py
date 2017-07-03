#!/usr/bin/env python2
"""This program helps organize and version your dot files with Git."""
import homekeeper.config
import homekeeper.util
import logging
import os
import shutil

__version__ = '4.0.0'

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

    def restore(self):
        """Restores all symlinks (inverse of link)."""
        home = os.getenv('HOME')
        if self.config.override:
            homekeeper.util.restore(self.config.base,
                                    home,
                                    excludes=self.config.excludes,
                                    cherrypicks=self.config.cherrypicks)
        homekeeper.util.restore(self.config.directory,
                                home,
                                excludes=self.config.excludes,
                                cherrypicks=self.config.cherrypicks)
        homekeeper.util.cleanup_symlinks(home)

    def link(self):
        """Symlinks all files and directories from your dotfiles directory into
        your home directory.
        """
        home = os.getenv('HOME')
        if self.config.override:
            homekeeper.util.create_symlinks(self.config.base,
                                            home,
                                            excludes=self.config.excludes,
                                            cherrypicks=self.config.cherrypicks)
        homekeeper.util.create_symlinks(self.config.directory,
                                        home,
                                        excludes=self.config.excludes,
                                        cherrypicks=self.config.cherrypicks)
        homekeeper.util.cleanup_symlinks(home)

