import homekeeper.config
import homekeeper.main
import logging
import os
import shutil

__version__ = '4.0.0'


class Homekeeper(object):
    """Organizes and versions your dot files."""

    def __init__(self, pathname=None, cleanup_symlinks=True):
        self.home = os.getenv('HOME')
        self.config = homekeeper.config.Config()
        self.config.cleanup_symlinks = cleanup_symlinks
        self.main = homekeeper.main.Main()
        if pathname:
            self.config.load(pathname)

    def init(self):
        """Writes a configuration file with cwd as the dotfiles directory.
        Configuration file is written as JSON, and will be removed if it exists
        already.  If configuration already exists, the new dotfiles directory
        path will be merged into existing configuration.
        """
        logging.info('setting dotfiles directory to %s', self.config.directory)
        self.config.dotfiles_directory = os.path.realpath(os.getcwd())
        self.config.save()

    def symlink(self):
        """Symlinks all files and directories from your dotfiles directory into
        your home directory.
        """
        if self.config.override:
            self.main.create_symlinks(self.config.base_directory, self.home,
                                      excludes=self.config.excludes)
        self.main.create_symlinks(self.config.dotfiles_directory, self.home,
                                  excludes=self.config.excludes)
        self.cleanup()

    def restore(self, cleanup_symlinks=True):
        """Restores all symlinks (inverse of link)."""
        self.main.restore_symlinks(self.config.dotfiles_directory, self.home,
                                   excludes=self.config.excludes)
        if self.config.override:
            self.main.restore_symlinks(self.config.base_directory, self.home,
                                       excludes=self.config.excludes)
        self.cleanup()

    def cleanup(self):
        """Cleans up symlinks in the home directory."""
        if self.config.cleanup_symlinks:
            self.main.cleanup_symlinks(self.home)
