Homekeeper
==========
This project helps me organize and version my dotfiles across multiple
computers.  It is useful to keep these dotfiles in sync so I don't get confused.
You may or may not find it useful.

My dotfiles repository is located here if you'd like to take a look:

    https://github.com/retiman/dotfiles

Homekeeper will read a `$HOME/.homekeeper.json` file for configuration, or create
one if it doesn't already exist.  The default configuration looks like this:

    {
        "dotfiles_directory": "/home/$USER/proj/dotfiles",·
        "excludes": [
            ".git",
            ".gitignore",
            "LICENSE",
            "README.md"
        ]
    }

Homekeeper will not symlink any file in the `excludes` array in the
configuration.  The default is to exclude the `.gitignore` and `.git` files
but you can change this if you want.

You may have homekeeper generate this file by running `homekeeper init` in the
directory where you store your dotfiles.

Once homekeeper knows where your dotfiles live, it will remove the dotfile in
your home directory, and symlink it from your dotfiles directory.  For example,
if you have a `.bash_profile` in `~/dotfiles`, then your home directory will
contain:

    .bash_profile -> /home/yourusername/dotfiles/.bash_profile

NOTE: HOMEKEEPER WILL REMOVE THE ORIGINAL FILE ONCE YOU TELL IT TO SYMLINK.

Make sure you back it up or are having homekeeper track the file you want to
symlink first.

Multiple Computers
==================
If you have multiple computers or VMs you are working with, consider making a
branch for each one.  I like to name each branch after a host I am working on.
If you like a commit and want them to show up in all branches, do this:

1.  `git commit -am "My super awesome change"`
1.  `git checkout master`
1.  `git cherry-pick <commitid>`
1.  `git checkout <host-branch>`
1.  `git merge master`

Or you can run `homekeeper save` which will do the same thing with what HEAD
points to in the current branch.

If you are on a different computer or VM and want to pick up the changes
from master, do this:

1.  `git checkout master`
1.  `git pull origin master`
1.  `git checkout <host-branch>`
1.  `git merge master`

Or you can run `homekeeper update` which will do the same thing.

More Documentation
==================
There isn't any.  I don't think anybody will use this except me.
