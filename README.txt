Homekeeper
----------
This project helps me organize and version my dotfiles.  You may find it useful.

I have a Git repository with a ``bin`` directory and a ``dotfiles`` directory, containing my
scripts and dotfiles, respectively.  They are versioned and symlinked to my home directory.

Your dotfiles should contain a ``.homekeeper.conf`` that describes where your dotfiles are,
as well as some other information.

Here is a sample ``.homekeeper.conf``:

``dotfiles_dir = '/home/minhuang/proj/dotfiles'
initial_dot = False``

Setting ``initial_dot = False`` means homekeeper will assume you have saved your dotfiles
without the initial dot.  For example, instead of ``.bash_profile``, you have saved it as
``bash_profile``.

Here is a sample run:

``Symlinking bin files
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
