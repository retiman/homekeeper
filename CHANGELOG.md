# Changelog

## 5.1.0 - 2020-07-15

- Added Python 3.7 support.
- Added Python 3.6 support.
- Added Sphinx generated docs.
- Changed README format to reStructured Text.
- Changed CHANGELOG format to reStructured Text.
- Removed make in favor of tox.

## 5.0.4 - 2020-07-15

- Fixes a problem with using Markdown when uploading to PyPI.
- Fixes various typos.

## 5.0.0 - 2020-07-11

- Added Python 3.5 support.
- Changed configuration format; now multiple directories will be considered (not just a base/dotfiles directory).
- Changed configuration key ``base_directory`` -> ``directories``.
- Changed configuration key ``dotfiles_directory`` -> ``directories``.
- Changed license to MIT license.
- Removed Python 2 support.
- Removed the configuration key ``includes``/``cherrypick`` temporarily; its need is being evaluated.
- Removed the ``link`` argument; use ``keep`` instead.
- Removed support for Git; arbitrary SCM tools are supported.

## 4.0.6 - 2019-04-01

- Last release to support Python 2.7.

## 2.2.3 - 2014-01-02

- Fixed a bug with deleting existing dotfile(s).

## 2.2.2 - 2013-12-07

- Fixed a bug that prevented working with different versions of Git.

## 2.2.0 - 2013-12-07

- Added support for Git 1.8.

## 2.1.2 - 2013-11-20

- Fixed a bug where spurious logging messages were displayed.
