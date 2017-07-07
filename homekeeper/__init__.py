import homekeeper.config
import logging
import os
import shutil

__version__ = '4.0.0'


class Homekeeper(object):
    """Organizes and versions your dot files."""

    def __init__(self, config_path=None):
        self.home = os.getenv('HOME')
        self.config = homekeeper.config.Config()
        self.config_path = (config_path if config_path
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
            homekeeper.core.create_symlinks(self.config.base_directory,
                                            self.home,
                                            excludes=self.config.excludes)
        homekeeper.core.create_symlinks(self.config.dotfiles_directory,
                                        self.home,
                                        excludes=self.config.excludes)
        self.cleanup()

    def link(self):
        self.keep()

    def unkeep(self):
        """Restores all symlinks (inverse of link)."""
        if self.config.override:
            homekeeper.core.restore_symlinks(self.config.base_directory,
                                             self.home,
                                             excludes=self.config.excludes)
        homekeeper.core.restore_symlinks(self.config.dotfiles_directory,
                                         self.home,
                                         excludes=self.config.excludes)
        self.cleanup()

    def restore(self):
        self.unkeep()

    def cleanup(self):
        """Cleans up symlinks in the home directory."""
        if self.config.cleanup_symlinks:
            homekeeper.core.cleanup_symlinks(self.home)

    @property
    def cleanup_symlinks(self):
        return self.config.cleanup_symlinks

    @property
    def overwrite(self):
        return self.config.overwrite

    @cleanup_symlinks.setter
    def cleanup_symlinks(self, value):
        self.config.cleanup_symlinks = value

    @overwrite.setter
    def overwrite(self, value):
        self.overwrite = value
