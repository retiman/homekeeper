import logging
import json
import os


def fopen(*args, **kwargs):
    """Alias for __builtin__.open. This exists so tests may mock this function
    without overriding open for all modules.
    """
    return open(*args, **kwargs)


class Config(object):
    """Representation of the homekeeper configuration file."""

    def __init__(self):
        self.base_directory = None
        self.dotfiles_directory = os.path.join(os.getenv('HOME'), 'dotfiles')
        self.excludes = ['.git', '.gitignore', 'LICENSE', 'README.md']
        self.override = False

    def load(self, pathname):
        with fopen(pathname, 'r') as f:
            data = json.loads(f.read())
            if 'base_directory' in data:
                self.base_directory = data['base_directory']
            if 'dotfiles_directory' in data:
                self.dotfiles_directory = data['dotfiles_directory']
            if 'excludes' in data:
                self.excludes = data['excludes']
            else:
                self.excludes = []
            self.override = self.base_directory is not None
            logging.info('loaded configuration from %s', pathname)

    def save(self, pathname):
        with fopen(pathname, 'w') as f:
            data = {
                'base_directory': self.base_directory,
                'dotfiles_directory': self.dotfiles_directory,
                'excludes': self.excludes,
            }
            f.write(json.dumps(data, sort_keys=True, indent=4))
            logging.info('saved configuration to %s', pathname)
