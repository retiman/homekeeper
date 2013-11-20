#!/usr/bin/env python2
import json
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


class Homekeeper(object):
    CONFIG_PATHNAME = os.path.join(os.getenv('HOME'), '.homekeeper.json')

    def __init__(self, overrides={}):
        defaults = {
            'dotfiles_directory': os.path.join(os.getenv('HOME'), 'dotfiles'),
            'excludes': ['.gitignore', 'LICENSE', 'README.md']
        }
        config_file = self.__parse_config()
        self.config = overrides
        self.config.update(config_file)
        self.config.update(defaults)

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
        if not os.path.isdir(source_directory):
            return
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

    def init(self):
        """Writes a configuration file with cwd as the dotfiles directory.

        Configuration file is written as JSON, and will be removed if it exists
        already.  If configuration already exists, the new dotfiles directory
        path will be merged into existing configuration.
        """
        self.config['dotfiles_directory'] = os.path.realpath(os.getcwd())
        serialized = json.dumps(self.config, sort_keys=True, indent=4)
        if os.path.exists(self.CONFIG_PATHNAME):
            print 'overwriting %s' % self.CONFIG_PATHNAME
            os.remove(self.CONFIG_PATHNAME)
        config = open(self.CONFIG_PATHNAME, 'w')
        config.write(serialized)
        config.close()
        print 'wrote configuration to %s' % self.CONFIG_PATHNAME

    def branch(self):
        with _cd(self.dotfiles_directory):
            return _sh('git status').split('\n')[0].split('# On branch ')[1]

    def commit_id(self):
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
            c = self.commit_id()
            _sh('git checkout master')
            _sh('git cherry-pick %s' % c)
            _sh('git checkout %s' % b)
            _sh('git merge master')

    def link(self):
        home_directory = os.getenv('HOME')
        self.__symlink_files(self.dotfiles_directory, home_directory,
                             initial_dot=True)
        if self.scripts_directory:
            self.__symlink_files(self.scripts_directory,
                                os.path.join(home_directory, 'bin'),
                                initial_dot=False)
        self.__remove_broken_symlinks(home_directory)
