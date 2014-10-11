#!/usr/bin/env python2
import json
import os

class Config(object):
    PATHNAME = os.path.join(os.getenv('HOME'), '.homekeeper.json')
    DEFAULTS = {
        'base': None,
        'directory': os.path.join(os.getenv('HOME'), 'dotfiles'),
        'excludes': ['.git', '.gitignore', 'LICENSE', 'README.md'],
        'override': False
        }

    def __init__(self, pathname=None):
        config = {}
        pathname = pathname or self.PATHNAME
        if os.path.exists(pathname):
            try:
                print 'found homekeeper configuration at %s' % pathname
                config = json.loads(open(self.PATHNAME).read())
            except ValueError:
                print 'homekeeper configuration invalid; assuming defaults'
                config = self.DEFAULTS
        else:
            print 'homekeeper configuration not found; assuming defaults'
            config = self.DEFAULTS
        self.base = config['base'] if 'base' in config else None
        self.directory = config['directory'] if 'directory' in config else None
        self.excludes = config['excludes'] if 'excludes' in config else []
        self.override = config['override'] if 'override' in config else False
        # This is the old configuration directive; it is retained and overrides
        # the normal directive if present.
        if 'dotfiles_directory' in config:
            self.directory = config['dotfiles_directory']
        self.config = config
        self.pathname = pathname
