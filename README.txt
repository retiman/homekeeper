[![Build Status](https://travis-ci.org/retiman/homekeeper.svg?branch=master)](https://travis-ci.org/retiman/homekeeper)

Homekeeper
==========
This project helps organize and by symlinking them from another location.  You may opt to version your dotfiles using
git or another SCM tool so you can have access to them easily while working on other machines.

In the event that you use multiple computers and would like dotfiles to be shared, you can list of dotfiles directories
that will be overridden.  This can be useful if you have your own personal dotfiles, but then want dotfiles for work
to be located in a separate directory or repository.

Installation
============
Install it via [pypi](https://pypi.python.org/pypi/homekeeper):

    pip install homekeeper
    
Versions 5.0.0 and above are compatible with Python 3 only.

Versions 4.0.5 and below are compatible with Python 2 only.

Usage
=====
Create a repository or directory to store your dotfiles (like [this one](https://github.com/retiman/dotfiles)), then
create a `$HOME/.homekeeper.json` that points to that repository.  Running `homekeeper keep` symlinks the dotfiles
from the repository to your home directory.


Configuration
=============
Homekeeper will read a `$HOME/.homekeeper.json` file for configuration.  A simple configuration looks like this:

    {
        "directories": [
            "/home/$USER/dotfiles/base",
            "/home/$USER/dotfiles/host"
        ]
        "excludes": [
            ".git",
            ".gitignore",
        ]
    }

Homekeeper will symlink files from each directory in order.  Homekeeper will not symlink any file in the `excludes`
array in the configuration.

For example, if you have a `.bash_profile` in `~/dotfiles`, then after running `homekeeper keep`, your home directory
will contain:

    .bash_profile -> /home/$USER/dotfiles/.bash_profile
    
NOTE: HOMEKEEPER WILL DELETE THE ORIGINAL FILE IN YOUR HOME DIRECTORY AND CREATE A SYMLINK.
  
To prevent homekeeper from doing this, run with the `--no-overwrite` flag (although this may prevent homekeeper from
doing anything useful).

Run `homekeeper unkeep` to undo this process.
