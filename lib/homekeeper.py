#!/usr/bin/env python2
import os
import subprocess
import sys

class cd(object):
    """Context manager for changing directories."""
    def __init__(self, pathname):
        self.pathname = pathname

    def __enter__(self):
        self.saved_pathname = os.getcwd()
        os.chdir(self.pathname)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_pathname)

def mkdir_p(pathname):
    try:
        os.makedirs(pathname)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise

def remove_broken_symlinks(directory):
    for pathname in os.listdir(directory):
        if not os.path.islink(pathname):
            continue
        if os.path.exists(os.readlink(pathname)):
            continue
        print 'removing broken link: %s' % pathname
        os.unlink(pathname)

def print_usage():
    print 'Usage: homekeeper [command]'
    print 'Commands:'
    print '  link              symlink dotfiles and remove broken symlinks.'
    print '  save              save the last commit in master branch.'
    print '  track             track the dotfile with homekeeper.'
    print '  update            pull from master and merge into this branch.'

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

def parse_config():
    config_pathname = os.path.join(os.getenv('HOME'), '.homekeeper.conf')
    if not os.path.exists(config_pathname):
        print 'please create a .homekeeper.conf file in your home directory.'
        sys.exit(1)
    config = {}
    execfile(config_pathname, config)
    if 'dotfiles' not in config:
        print 'homekeeper configuration requires a "dotfiles" variable set.'
        sys.exit(1)
    return config

def branch(config):
    with cd(config['dotfiles']):
        return sh(['git', 'status']).split('\n')[0].split('# On branch ')[1]

def commit(config):
    with cd(config['dotfiles']):
        return sh(['git', 'show', 'HEAD']).split('\n')[0].split(' ')[1]

def update(config):
    with cd(config['dotfiles']):
        b = branch()
        sh('git fetch')
        sh('git merge origin/%s' % b)
        sh('git checkout master')
        sh('git merge origin/master')
        sh('git checkout %s' % b)
        sh('git merge master')

def save(config):
    with cd(config['dotfiles']):
        b = branch
        c = commit
        sh('git checkout master')
        sh('git cherry-pick %s' % c)
        sh('git checkout %s' % b)
        sh('git merge master')

def link(config):
    with cd(config['dotfiles']):
        shutil.rmtree('tmp')
        mkdir_p(os.path.join('originals', 'bin'))
        mkdir_p(os.path.join('originals', 'dotfiles'))
        home = os.getenv('HOME')

        print 'symlinking bin files.'
        for pathname in os.listdir('bin'):
            basename = os.path.basename(pathname)
            original = os.path.join(home, 'bin', basename).strip()
            if os.path.exists(original):
                shutil.copyfile(original, os.path.join('originals', 'bin'))
                shutil.rmtree(original)
            os.symlink(pathname, original)
            print 'symlinked %s' % original

        print 'symlinking dotfiles.'
        for pathname in os.listdir('dotfiles'):
            basename = os.path.basename(pathname)
            original = os.path.join(home, 'bin', '.' + basename).strip()
            if os.path.exists(original):
                shutil.copyfile(original, os.path.join('originals', 'dotfiles'))
                shutil.rmtree(original)
            os.symlink(pathname, original)
            print 'symlinked %s' % original

        print 'removing broken symlinks.'
        remove_broken_symlinks
