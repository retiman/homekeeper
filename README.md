# Homekeeper

This project helps organize dotfiles by symlinking them from another location.  You may opt to version your dotfiles
using git or another SCM tool so you can have access to them easily while working on other machines.

```
Homekeeper symlinks dotfiles to your home directory.

Usage:
  homekeeper [command]

Available Commands:
  cleanup     Removes broken symlinks in your home directory.
  completion  generate the autocompletion script for the specified shell
  help        Help about any command
  init        Sets your dotfiles directory, possibly from a git clone.
  keep        Symlinks dotfiles to your home directory from another location.
  unkeep      Replaces symlinks in your home directory with symlinked files.
  version     Prints the version and then exists.

Flags:
      --debug     Enables debug output in addition to normal output.
      --dry-run   Enables dry run mode (no changes will be made).
  -h, --help      help for homekeeper
      --quiet     Enables quiet mode (will not output anything)

Use "homekeeper [command] --help" for more information about a command.
```

## Installation

### Versions 5.x.x

Versions 5.x.x are compatible with Python 3 only.  Install it via `pip`:

`pip install homekeeper==5.1.0`

Previous versions of homekeeper are configuration with JSON and not YAML.

### Versions 4.x.x

Versions 4.0.5 and below are compatible with Python 2 only.  Install it via `pip`:

`pip install homekeeper==4.0.5`

Previous versions of homekeeper are configuration with JSON and not YAML.

## Usage

If you have your dotfiles stored in GitHub, just run homekeeper in the directory you want to repository to be cloned:

```
cd /home/johndoe/git/repositories
homekeeper init --debug --git https://github.com/johndoe/dotfiles.git
```

This will symlink all files in `$HOME/git/repositories` to your home directory.  If you've already cloned your dotfiles repository, create a `.homekeeper.yml` and place it in your `$HOME` directory:

```
directories:
  - /home/johndoe/git/repositories/dotfiles
ignores:
  - .env
  - .git
```

Add additional directories to the configuration file to have other dotfiles take precendence.  Any ignored files won't be symlinked (by default the `.git` directory is ignored).

Run `homekeeper keep` to refresh the symlinks if you add new files, or `homekeeper unkeep` to reverse this process.

## Contributing

To release:

1. Bump the version in `VERSION`.
1. Run `make tag` to tag the release.
1. Run `git push origin --tags` to push the tags and trigger the `release` workflow.
