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
        self.data = self.DEFAULTS
        self.pathname = os.path.realpath(pathname or self.PATHNAME)
        if not os.path.exists(self.pathname):
            print 'homekeeper configuration not found; assuming defaults'
            return
        try:
            print 'found homekeeper configuration at %s' % self.pathname
            self.data = json.loads(open(self.pathname).read())
        except ValueError:
            print 'homekeeper configuration invalid; assuming defaults'
        if 'dotfiles_directory' in self.data:
            self.data['directory'] = self.data['dotfiles_directory']
            del self.data['dotfiles_directory']
        if self.directory == os.path.realpath(os.getenv('HOME')):
            print 'your dotfiles directory cannot be your home directory'
            self.data['directory'] = self.DEFAULTS['directory']
            return

    def save(self, pathname=None):
        pathname = pathname or self.pathname
        if os.path.exists(pathname):
            print 'overwriting %s' % pathname
            os.remove(pathname)
        with open(pathname, 'w') as cfile:
            cfile.write(json.dumps(self.data, sort_keys=True, indent=4))

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

