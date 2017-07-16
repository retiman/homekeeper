import homekeeper.config
import homekeeper.core
import logging
import os
import shutil

__version__ = '4.0.1'
core = homekeeper.core


class Homekeeper(object):
    """Organizes and versions your dot files."""

    def __init__(self, config_path=None):
        self.config_path = config_path
        self.config = homekeeper.config.Config()
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
        core.create_symlinks_from_base(self.config)
        core.create_symlinks_from_dotfiles(self.config)
        self.cleanup()

    def link(self):
        self.keep()

    def unkeep(self):
        """Restores all symlinks (inverse of link)."""
        core.restore_symlinks_from_base(self.config)
        core.restore_symlinks_from_dotfiles(self.config)
        self.cleanup()

    def restore(self):
        self.unkeep()

    def cleanup(self):
        """Cleans up symlinks in the home directory."""
        if not self.config.cleanup_symlinks:
            logging.info('skipping cleanup of broken symlinks')
            return
        core.cleanup_symlinks(self.config.home)

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
        self.config.overwrite = value
