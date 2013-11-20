Homekeeper
----------
This project helps me organize and version my dotfiles.  You may find it useful.

I have a Git repository with a ``bin`` directory and a ``dotfiles`` directory,
containing my scripts and dotfiles, respectively.  They are versioned and
symlinked to my home directory.

Your dotfiles should contain a ``.homekeeper.conf`` that describes where your
dotfiles are.

Here is a sample ``.homekeeper.conf``:

``dotfiles_directory = '/home/minhuang/proj/personal/dotfiles'``

If you don't create a ``homekeeper.conf``, homekeeper will assume your dotfiles
are in ``/home/$USER/proj/dotfiles/lib``.

A special exception is made for a scripts directory; if you have one, it will
be symlinked to ``bin`` in your home directory unless you specify:

``scripts_directory = '/home/minhuang/scripts`` or something else.  Setting this
value to ``None`` will disable this feature.

Here is a sample run:

``Symlinking scripts
Symlinked: /home/minhuang/bin/pushkey
Symlinked: /home/minhuang/bin/lein
Symlinked: /home/minhuang/bin/define
Symlinking dot files
Symlinked: /home/minhuang/.gemrc
Symlinked: /home/minhuang/.ctags
Symlinked: /home/minhuang/.toprc
Symlinked: /home/minhuang/.gitignore
Symlinked: /home/minhuang/.i3status.conf
Symlinked: /home/minhuang/.tpbrc
Symlinked: /home/minhuang/.gntrc
Symlinked: /home/minhuang/.gitk
Symlinked: /home/minhuang/.gvimrc
Symlinked: /home/minhuang/.bash_functions
Symlinked: /home/minhuang/.dircolors
Symlinked: /home/minhuang/.vim
Symlinked: /home/minhuang/.gbp.conf
Symlinked: /home/minhuang/.xinitrc
Symlinked: /home/minhuang/.vimrc
Symlinked: /home/minhuang/.kderc
Symlinked: /home/minhuang/.screenrc
Symlinked: /home/minhuang/.bash_profile
Symlinked: /home/minhuang/.i3
Symlinked: /home/minhuang/.irbrc
Symlinked: /home/minhuang/.bash_aliases
Symlinked: /home/minhuang/.Xdefaults
Symlinked: /home/minhuang/.gtkrc-2.0
Symlinked: /home/minhuang/.gitconfig
Symlinked: /home/minhuang/.muttrc
Removing broken symlinks``

Multiple Computers
------------------
If you have multiple computers or VMs you are working with, consider making a
branch for each one.  I like to name each branch after a host I am working on.
If you like a commit and want them to show up in all branches, do this:

1.  `git commit -am "My super awesome change"`
1.  `git checkout master`
1.  `git cherry-pick COMMITID`
1.  `git checkout HOST`
1.  `git merge master`

Or you can run `homekeeper save` which will do the same thing with what HEAD
points to in the current branch.

If you are on a different computer or VM and want to pick up the changes
from master, do this:

1.  `git checkout master`
1.  `git pull origin master`
1.  `git checkout HOST`
1.  `git merge master`

Or you can run `homekeeper update` which will do the same thing.

More Documentation
------------------
There isn't any.  I don't think anybody will use this except me.
