import homekeeper.config
import logging
import os
import shutil

from homekeeper import core

__version__ = '4.0.0'


class Homekeeper(object):
    """Organizes and versions your dot files."""

    def __init__(self, pathname=None, cleanup_symlinks=True):
        self.home = os.getenv('HOME')
        self.config = homekeeper.config.Config()
        self.config.cleanup_symlinks = cleanup_symlinks
        self.config_path = (pathname if pathname
                            else os.path.join(self.home, '.homekeeper.json'))
        self.config.load(self.config_path)

    def init(self):
        """Writes a configuration file with cwd as the dotfiles directory.
        Configuration file is written as JSON, and will be removed if it exists
        already.  If configuration already exists, the new dotfiles directory
        path will be merged into existing configuration.
        """
        dotfiles_directory = os.path.realpath(os.getcwd())
        logging.info('setting dotfiles directory to %s', dotfiles_directory)
        self.config.dotfiles_directory = os.path.realpath(os.getcwd())
        self.config.save(self.config_path)

    def keep(self):
        """Symlinks all files and directories from your dotfiles directory into
        your home directory.
        """
        if self.config.override:
            core.create_symlinks(self.config.base_directory, self.home,
                                 excludes=self.config.excludes)
        core.create_symlinks(self.config.dotfiles_directory, self.home,
                             excludes=self.config.excludes)
        self.cleanup()

    def link(self):
        self.keep()

    def unkeep(self):
        """Restores all symlinks (inverse of link)."""
        core.restore_symlinks(self.config.dotfiles_directory, self.home,
                              excludes=self.config.excludes)
        if self.config.override:
            core.restore_symlinks(self.config.base_directory, self.home,
                                  excludes=self.config.excludes)
        self.cleanup()

    def restore(self):
        self.unkeep()

    def cleanup(self):
        """Cleans up symlinks in the home directory."""
        if self.config.cleanup_symlinks:
            core.cleanup_symlinks(self.home)
