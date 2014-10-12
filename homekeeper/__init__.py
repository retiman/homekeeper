#!/usr/bin/env python2
"""This program helps organize and version your dot files with Git."""
import homekeeper.config
import homekeeper.util
import json
import os
import shutil
import subprocess
import sys

Config = homekeeper.config.Config

__version__ = '3.0.0'

class Homekeeper(object):
    """Organizes and versions your dot files."""

    def __init__(self, pathname=None):
        self.config = Config(pathname)

    def init(self):
        """Writes a configuration file with cwd as the dotfiles directory.

        Configuration file is written as JSON, and will be removed if it exists
        already.  If configuration already exists, the new dotfiles directory
        path will be merged into existing configuration.
        """
        pathname = os.path.realpath(os.getcwd())

        self.config['dotfiles_directory'] = dotfiles_directory
        print 'setting dotfiles directory to %s' % os.getcwd()
        serialized = json.dumps(self.config, sort_keys=True, indent=4)
        if os.path.exists(Config.PATHNAME):
            print 'overwriting %s' % Config.PATHNAME
            os.remove(Config.PATHNAME)
        config = open(Config.PATHNAME, 'w')
        config.write(serialized)
        config.close()
        print 'wrote configuration to %s' % Config.PATHNAME

    def track(self, pathname):
        if not os.path.exists(pathname):
            print "pathname not found; won't track %s" % pathname
            return
        basename = os.path.basename(pathname)
        target = os.path.join(self.config['dotfiles_directory'], basename)
        if os.path.exists(target):
            print 'this path is already tracked at %s' % target
            return
        print 'moved %s to %s' % (pathname, target)
        shutil.move(pathname, target)

    def link(self):
        homekeeper.util.create_symlinks(self.config)
        homekeeper.util.cleanup_symlinks(home_directory)
