#!/usr/bin/env python2
import os
import shutil
import subprocess
import sys


class _cd(object):
    def __init__(self, pathname):
        self.pathname = pathname

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
    p = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out


class ConfigurationError(Exception):
    pass


class Homekeeper(object):

    def __init__(self, config_pathname=None):
        self.config_pathname = config_pathname
        if not self.config_pathname:
            self.config_pathname = os.path.join(os.getenv('HOME'),
                                                '.homekeeper.conf')
        if not os.path.exists(self.config_pathname):
            raise ConfigurationError(".homekeeper.conf doesn't exist.")
        self.config = {}
        execfile(self.config_pathname, self.config)
        if 'dotfiles_directory' not in self.config:
            raise ConfigurationError('homekeeper configuration requires a '
                                     '"dotfiles_dir" variable set.')
        self.dotfiles_directory = self.config['dotfiles_directory']
        self.scripts_directory = self.config.get('scripts_directory', '')
        self.initial_dot = self.config.get('initial_dot', False)

    def __mkdir_p(self, pathname):
        try:
            os.makedirs(pathname)
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass
            else:
                raise

    def __remove_broken_symlinks(self, directory):
        for pathname in os.listdir(directory):
            if not os.path.islink(pathname):
                continue
            if os.path.exists(os.readlink(pathname)):
                continue
            print 'removing broken link: %s' % pathname
            os.unlink(pathname)

    def __symlink_files(self, target_directory, initial_dot=False):
        print 'symlinking files to %s' % target_directory
        for pathname in os.listdir('.'):
            basename = os.path.basename(pathname)
            if initial_dot:
                original = os.path.join(target_directory, '.', basename)
            else:
                original = os.path.join(target_directory, basename)
            if os.path.exists(original):
                shutil.rmtree(original)
            os.symlink(pathname, original)
            print 'symlinked %s' % original

    def branch(self):
        with _cd(self.dotfiles_directory):
            return _sh('git status').split('\n')[0].split('# On branch ')[1]

    def commit(self):
        with _cd(self.dotfiles_directory):
            return _sh('git show HEAD').split('\n')[0].split(' ')[1]

    def update(self):
        with _cd(self.dotfiles_directory):
            b = self.branch()
            _sh('git fetch')
            _sh('git merge origin/%s' % b)
            _sh('git checkout master')
            _sh('git merge origin/master')
            _sh('git checkout %s' % b)
            _sh('git merge master')

    def save(self):
        with _cd(self.dotfiles_directory):
            b = self.branch()
            c = self.commit()
            _sh('git checkout master')
            _sh('git cherry-pick %s' % c)
            _sh('git checkout %s' % b)
            _sh('git merge master')

    def link(self):
        home_directory = os.getenv('HOME')
        with _cd(self.dotfiles_directory):
            target_directory = os.path.join(home_directory)
            self.__symlink_files(target_directory, initial_dot=self.initial_dot)
        with _cd(self.scripts_directory):
            target_directory = os.path.join(home_directory, 'bin')
            self.__symlink_files(target_directory, initial_dot=False)
        self.__remove_broken_symlinks()
