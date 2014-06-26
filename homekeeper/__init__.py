#!/usr/bin/env python2
"""This program helps organize and version your dot files with Git."""
import json
import os
import shutil
import subprocess
import sys

__version__ = '2.3.0'

class _cd(object):
    "Use with the `with` keyword to change directory."""
    def __init__(self, pathname):
        self.pathname = pathname
        self.saved_pathname = None

    def __enter__(self):
        self.saved_pathname = os.getcwd()
        os.chdir(self.pathname)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_pathname)

def _sh(command):
    """Prints a command executes it.

    Args:
        command: The command to execute.

    Returns:
        The output of the command, discarding anything printed to standard
        error.
    """
    print command
    proc = subprocess.Popen(command.split(' '),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, _ = proc.communicate()
    return out

def _remove_broken_symlinks(directory):
    """Removes broken symlinks from a directory.

    Args:
        directory: The directory to look for broken symlinks.
    """
    for pathname in os.listdir(directory):
        pathname = os.path.join(directory, pathname)
        if not os.path.islink(pathname):
            continue
        if os.path.exists(os.readlink(pathname)):
            continue
        print 'removing broken link: %s' % pathname
        os.unlink(pathname)

class Homekeeper(object):
    """Organizes and versions your dot files."""
    CONFIG_PATHNAME = os.path.join(os.getenv('HOME'), '.homekeeper.json')
    CONFIG_DEFAULTS = {
        'dotfiles_directory': os.path.join(os.getenv('HOME'), 'dotfiles'),
        'excludes': ['.git', '.gitignore', 'LICENSE', 'README.md']
        }

    def __init__(self, overrides=None):
        if overrides is None:
            overrides = {}
        self.config = self.CONFIG_DEFAULTS
        self.config.update(self.__parse_config())
        self.config.update(overrides)
        if self.config['dotfiles_directory'] == os.getenv('HOME'):
            raise ValueError('your dotfiles directory cannot be your home '
                             'directory')

    def __parse_config(self):
        if not os.path.exists(self.CONFIG_PATHNAME):
            print 'homekeeper configuration not found; assuming defaults'
            return {}
        try:
            config = json.loads(open(self.CONFIG_PATHNAME).read())
            print 'found homekeeper configuration at %s' % self.CONFIG_PATHNAME
            return config
        except ValueError:
            print 'homekeeper configuration invalid; assuming defaults'
            return {}

    def __symlink_files(self, source_directory, target_directory):
        if not os.path.isdir(source_directory):
            print 'dotfiles directory not found: %s' % source_directory
            return
        print 'symlinking files from %s' % source_directory
        with _cd(source_directory):
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
        if os.path.exists(self.CONFIG_PATHNAME):
            print 'overwriting %s' % self.CONFIG_PATHNAME
            os.remove(self.CONFIG_PATHNAME)
        config = open(self.CONFIG_PATHNAME, 'w')
        config.write(serialized)
        config.close()
        print 'wrote configuration to %s' % self.CONFIG_PATHNAME

    def branch(self):
        with _cd(self.config['dotfiles_directory']):
            return _sh('git status').split('\n')[0].split()[-1]

    def commit_id(self):
        with _cd(self.config['dotfiles_directory']):
            return _sh('git show HEAD').split('\n')[0].split(' ')[1]

    def update(self):
        with _cd(self.config['dotfiles_directory']):
            branch = self.branch()
            _sh('git fetch')
            _sh('git merge origin/%s' % branch)
            _sh('git checkout master')
            _sh('git merge origin/master')
            _sh('git checkout %s' % branch)
            _sh('git merge master')

    def save(self):
        with _cd(self.config['dotfiles_directory']):
            branch = self.branch()
            commit = self.commit_id()
            if commit == 'master':
                print "nothing to save; you're already on master."
                return
            _sh('git checkout master')
            _sh('git cherry-pick %s' % commit)
            _sh('git checkout %s' % branch)
            _sh('git merge master')

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
        _remove_broken_symlinks(home_directory)
