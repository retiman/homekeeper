#!/usr/bin/env python2
import os
import subprocess
import sys


class ConfigurationError(Exception):
    pass


class Homekeeper(object):
    class _cd(object):
        def __init__(self, pathname):
            self.pathname = pathname

        def __enter__(self):
            self.saved_pathname = os.getcwd()
            os.chdir(self.pathname)

        def __exit__(self, etype, value, traceback):
            os.chdir(self.saved_pathname)

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

    def __mkdir_p(pathname):
        try:
            os.makedirs(pathname)
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass
            else:
                raise

    def __remove_broken_symlinks(directory):
        for pathname in os.listdir(directory):
            if not os.path.islink(pathname):
                continue
            if os.path.exists(os.readlink(pathname)):
                continue
            print 'removing broken link: %s' % pathname
            os.unlink(pathname)

    def __symlink_files(initial_dot=False):
        print 'symlinking files in %s' % source_directory
        home_directory = os.getenv('HOME')
        for pathname in os.listdir('.'):
            basename = os.path.basename(pathname)
            if initial_dot:
                original = os.path.join(home_directory, source_directory,
                                        '.', basename)
            else:
                original = os.path.join(home_directory, source_directory,
                                        basename)
            if os.path.exists(original):
                shutil.rmtree(original)
            os.symlink(pathname, original)
            print 'symlinked %s' % original

    def sh(command):
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

    def branch():
        with _cd(self.dotfiles_directory):
            return sh(['git', 'status']).split('\n')[0].split('# On branch ')[1]

    def commit():
        with _cd(self.dotfiles_directory):
            return sh(['git', 'show', 'HEAD']).split('\n')[0].split(' ')[1]

    def update():
        with _cd(self.dotfiles_directory):
            b = branch()
            sh('git fetch')
            sh('git merge origin/%s' % b)
            sh('git checkout master')
            sh('git merge origin/master')
            sh('git checkout %s' % b)
            sh('git merge master')

    def save():
        with _cd(self.dotfiles_directory):
            b = branch
            c = commit
            sh('git checkout master')
            sh('git cherry-pick %s' % c)
            sh('git checkout %s' % b)
            sh('git merge master')

    def link():
        with _cd(self.dotfiles_directory):
            self.__symlink_files(initial_dot=self.initial_dot)
        with _cd(self.scripts_directory):
            self.__symlink_files(initial_dot=False)
        self.__remove_broken_symlinks()
