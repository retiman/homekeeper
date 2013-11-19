#!/usr/bin/env python2
import optparse
import os
import shutil
import subprocess
import sys

def print_usage():
    print 'Usage: homekeeper [command]'
    print 'Commands:'
    print '  link              symlink dotfiles and remove broken symlinks.'
    print '  save              save the last commit in master branch.'
    print '  track             track the dotfile with homekeeper.'
    print '  update            pull from master and merge into this branch.'

def sh(command_array):
    print ' '.join(command_array)
    p = subprocess.Popen(command_array, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out

def branch():
    return sh(['git', 'status']).split('\n')[0].split('# On branch ')[1]

def commit():
    return sh(['git', 'show', 'HEAD']).split('\n')[0].split(' ')[1]

if len(sys.argv) == 1:
    print_usage()
    sys.exit(0)
