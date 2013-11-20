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
    def __init__(self, config={}):
        self.config = config
        if 'dotfiles_directory' not in self.config:
            raise ConfigurationError('homekeeper configuration requires a '
                                     '"dotfiles_dir" variable set.')
        self.dotfiles_directory = self.config['dotfiles_directory']
        self.scripts_directory = self.config.get('scripts_directory', '')

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
            pathname = os.path.join(directory, pathname)
            if not os.path.islink(pathname):
                continue
            if os.path.exists(os.readlink(pathname)):
                continue
            print 'removing broken link: %s' % pathname
            os.unlink(pathname)

    def __symlink_files(self, source_directory, target_directory,
                        initial_dot=False):
        print 'symlinking files from %s' % source_directory
        with _cd(source_directory):
            for pathname in os.listdir('.'):
                basename = os.path.basename(pathname)
                source = os.path.join(source_directory, basename)
                if initial_dot:
                    basename = '.' + basename
                target = os.path.join(target_directory, basename)
                if os.path.islink(target):
                    os.unlink(target)
                if os.path.exists(target):
                    shutil.rmtree(target)
                os.symlink(source, target)
                print 'symlinked %s' % target

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
        self.__symlink_files(self.dotfiles_directory, home_directory,
                             initial_dot=True)
        self.__symlink_files(self.scripts_directory,
                             os.path.join(home_directory, 'bin'),
                             initial_dot=False)
        self.__remove_broken_symlinks(home_directory)
