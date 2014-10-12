#!/usr/bin/env python2
"""This program helps organize and version your dot files with Git."""
import homekeeper.config
import homekeeper.util
import json
import os
import shutil
import subprocess
import sys

# pylint: disable=invalid-name
cd = homekeeper.util.cd
# pylint: disable=invalid-name
sh = homekeeper.util.sh
Config = homekeeper.config.Config

__version__ = '3.0.0'

class Homekeeper(object):
    """Organizes and versions your dot files."""

    def __init__(self, pathname=None):
        self.config = Config(pathname)

    def __symlink_files(self, source_directory, target_directory):
        if not os.path.isdir(source_directory):
            print 'dotfiles directory not found: %s' % source_directory
            return
        print 'symlinking files from %s' % source_directory
        with cd(source_directory):
            excludes = set(self.config['excludes'])
            for pathname in os.listdir('.'):
                basename = os.path.basename(pathname)
                if basename in excludes:
                    continue
                source = os.path.join(source_directory, basename)
                target = os.path.join(target_directory, basename)
                if os.path.islink(target):
                    os.unlink(target)
                if os.path.isfile(target):
                    os.remove(target)
                if os.path.isdir(target):
                    shutil.rmtree(target)
                os.symlink(source, target)
                print 'symlinked %s' % target

    def init(self, dotfiles_directory=None):
        """Writes a configuration file with cwd as the dotfiles directory.

        Configuration file is written as JSON, and will be removed if it exists
        already.  If configuration already exists, the new dotfiles directory
        path will be merged into existing configuration.
        """
        if dotfiles_directory is None:
            dotfiles_directory = os.getcwd()
        dotfiles_directory = os.path.realpath(dotfiles_directory)
        if dotfiles_directory == os.path.realpath(os.getenv('HOME')):
            print 'your dotfiles directory cannot be your home directory'
            return
        self.config['dotfiles_directory'] = dotfiles_directory
        print 'setting dotfiles directory to %s' % os.getcwd()
        serialized = json.dumps(self.config, sort_keys=True, indent=4)
        if os.path.exists(Config.PATHNAME):
            print 'overwriting %s' % Config.PATHNAME
            os.remove(Config.PATHNAME)
        config = open(Config.PATHNAME, 'w')
        config.write(serialized)
        config.close()
        print 'wrote configuration to %s' % self.CONFIG_PATHNAME

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
        home_directory = os.getenv('HOME')
        self.__symlink_files(self.config['dotfiles_directory'], home_directory)
        homekeeper.util.cleanup_symlinks(home_directory)
