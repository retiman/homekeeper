[![Build Status](https://travis-ci.org/retiman/homekeeper.svg?branch=master)](https://travis-ci.org/retiman/homekeeper)

Homekeeper
==========
NOTE: The format for homekeeper configuration has changed; this change is not
backwards compatible with the old version.

This project helps organize and dotfiles across multiple (even across multiple
computers).  It does so by marking a directory as your 'dotfiles directory' and
then symlinking those files into your HOME directory.

In the event that you use multiple computers and would like dotfiles to be
shared, you can specify a 'base' dotfiles directory and have host specific
dotfiles override them.

One benefit of doing this is you can easily version your dotfiles directory with
the revision control system of your choice.

Examples
========

My dotfiles repository is located here if you'd like to take a look:

    https://github.com/retiman/dotfiles

How It Works
============

Homekeeper will read a `$HOME/.homekeeper.json` file for configuration, or
create one if it doesn't already exist.  The default configuration looks like
this:

    {
        "base": "/home/$USER/dotfiles/base",
        "directory": "/home/$USER/dotfiles/$HOST",
        "override": true,
        "excludes": [
            ".git",
            ".gitignore",
        ],
        "cherrypicks": [
            ".mplayer/config",
            ".config/Terminal/terminalrc",
        ],
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

Tracking
========

    $ homekeeper track ~/.vimrc

This will copy your `~/.vimrc` file into your dotfiles directory.  The next time
you run `homekeeper link` the original `~/.vimrc` will be deleted, and the
tracked version will be symlinked there instead.

If you track a directory, the entire directory and all subdirectories will be
copied to your dotfiles directory.  You can only track a top level directory.
For example, if you decide to track:

    $ homekeeper track ~/.foo/bar/baz

...then homekeeper will copy the `baz` directory into your dotfiles directory.
In order to track all files and directories under `.foo`, track the following:

    $ homekeeper track ~/.foo

If you want to track *just* `~/.foo/bar/baz`, see the section about cherrypicks
below.

Excludes
========

Any paths listed in the `excludes` directive in `homekeeper.json` will be
ignored by homekeeper when linking.  The only exception is if the path is also
in the `cherrypicks` directive (see below).

Cherry Picks
============

This directive tells homekeeper to 'cherry pick' a particular path for linking.
This is useful if you want to version control a single file, but not the other
files in the same directory, or any of the parent directories.

Once you have done so, copy the file manually (with the appropriate directory
structure) into your dotfiles directory.

NOTE: This feature is experimental and may change.

