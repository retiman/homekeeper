#!/usr/bin/env python2
import homekeeper.util
import logging
import json
import os

util = homekeeper.util

class Config(object):
    """Representation of the homekeeper configuration file (homekeeper.json)."""

    PATHNAME = os.path.join(os.getenv('HOME'), '.homekeeper.json')
    DEFAULTS = {
        'base': None,
        'directory': os.path.join(os.getenv('HOME'), 'dotfiles'),
        'excludes': ['.git', '.gitignore', 'LICENSE', 'README.md'],
        'cherrypicks': [],
        'override': False
    }

    def __init__(self, pathname=None):
        self.data = self.DEFAULTS
        self.pathname = self.PATHNAME
        if pathname is None:
            logging.info('homekeeper configuration not specified; assuming '
                         'defaults')
            return
        self.pathname = os.path.realpath(pathname)
        if not os.path.exists(self.pathname):
            logging.info('homekeeper configuration not found; assuming '
                         'defaults')
            return
        try:
            logging.info('found homekeeper configuration at %s', self.pathname)
            self.data = json.loads(util.fopen(self.pathname).read())
        except ValueError:
            logging.info('homekeeper configuration invalid; assuming defaults')
        if 'dotfiles_directory' in self.data:
            self.data['directory'] = self.data['dotfiles_directory']
            del self.data['dotfiles_directory']
        if self.directory == os.path.realpath(os.getenv('HOME')):
            logging.info('your dotfiles directory cannot be your home '
                         'directory')
            self.data['directory'] = self.DEFAULTS['directory']
            return

    def reset(self):
        self.data = self.DEFAULTS

    def save(self, pathname=None):
        """Saves the configuration data to a file. Existing configuration will
        be removed.

        Args:
            pathname: The file to save the configuration to.
        """
        pathname = pathname or self.pathname
        if os.path.exists(pathname):
            os.remove(pathname)
        with util.fopen(pathname, 'w') as cfile:
            cfile.write(json.dumps(self.data, sort_keys=True, indent=4))
        logging.info('saved configuration to %s', pathname)

    @property
    def base(self):
        return self.data.get('base', self.DEFAULTS['base'])

    @base.setter
    def base(self, value):
        self.data['base'] = value

    @property
    def excludes(self):
        return self.data.get('excludes', self.DEFAULTS['excludes'])

    @excludes.setter
    def excludes(self, value):
        self.data['excludes'] = value

    @property
    def cherrypicks(self):
        return self.data.get('cherrypicks', self.DEFAULTS['cherrypicks'])

    @cherrypicks.setter
    def cherrypicks(self, value):
        self.data['cherrypicks'] = value

    @property
    def override(self):
        return self.data.get('override', self.DEFAULTS['override'])

    @override.setter
    def override(self, value):
        self.data['override'] = value

    @property
    def directory(self):
        return self.data.get('directory', self.DEFAULTS['directory'])

    @directory.setter
    def directory(self, value):
        self.data['directory'] = value

