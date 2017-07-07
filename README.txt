[![Build Status](https://travis-ci.org/retiman/homekeeper.svg?branch=master)](https://travis-ci.org/retiman/homekeeper)

Homekeeper
==========
This project helps organize and version dotfiles.  You can keep your dotfile
in a repository somewhere, then symlink them into your HOME directory.  This
allows you to keep your dotfiles versioned and have them available on any
computer you use.

In the event that you use multiple computers and would like dotfiles to be
shared, you can specify a 'base' dotfiles directory and have host specific
dotfiles override them.

Installation
============
Install it via [pypi](https://pypi.python.org/pypi/homekeeper):

    pip install homekeeper

Examples
========

My dotfiles repository is located [here](https://github.com/retiman/dotfiles)
if you'd like to take a look.


How It Works
============

Homekeeper will read a `$HOME/.homekeeper.json` file for configuration, or
create one if it doesn't already exist.  The default configuration looks like
this:

    {
        "base_directory": "/home/$USER/dotfiles/base",
        "dotfiles_directory": "/home/$USER/dotfiles/$HOST",
        "excludes": [
            ".git",
            ".gitignore",
        ]
    }

Homekeeper will not symlink any file in the `excludes` array in the
configuration.

Homekeeper will symlink files in the base directory first, then override those
symlinks with files in your normal dotfiles directory.  This can be useful if
you have different configurations for different machines.

You may have homekeeper generate this file by running `homekeeper init` in the
directory where you store your dotfiles.

Once homekeeper knows where your dotfiles live, it will remove the dotfile in
your home directory, and symlink it from your dotfiles directory.  For example,
if you have a `.bash_profile` in `~/dotfiles`, then your home directory will
contain:

    .bash_profile -> /home/$USER/dotfiles/.bash_profile

NOTE: HOMEKEEPER WILL REMOVE THE ORIGINAL FILE ONCE YOU TELL IT TO SYMLINK.

Make sure you back it up or are having homekeeper track the file you want to
symlink first.

Excludes
========

Any paths listed in the `excludes` directive in `homekeeper.json` will be
ignored by homekeeper when linking.  The only exception is if the path is also
in the `cherrypicks` directive (see below).
