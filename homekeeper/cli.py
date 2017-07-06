import click
import homekeeper
import logging
import sys


logging.basicConfig(format='%(message)s', level=logging.INFO)

@click.command(short_help='set dotfiles directory to current directory')
@click.argument('config', type=click.Path(exists=True, dir_okay=False))
def init(config):
    homekeeper.Homekeeper().init(config)


@click.command(short_help='symlink dotfiles to home directory')
def link():
    homekeeper.Homekeeper().link()


@click.command(short_help='restore all symlinks in home directory')
def restore():
    homekeeper.Homekeeper().restore()

@click.command(short_help='restore all symlinks in home directory')
def unlink():
    restore()


@click.group()
def main():
    pass


main.add_command(init)
main.add_command(link)
main.add_command(restore)
main.add_command(unlink)
