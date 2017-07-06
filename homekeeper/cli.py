import click
import homekeeper
import logging
import sys


logging.basicConfig(format='%(message)s', level=logging.INFO)


@click.command(short_help='removes broken symlinks only')
@click.pass_context
def clean(ctx):
    h = homekeeper.Homekeeper(cleanup_symlinks=True)
    h.cleanup()


@click.command(short_help='set dotfiles directory to current directory')
@click.pass_context
def init(ctx):
    h = homekeeper.Homekeeper(config_path=ctx.obj['config_path'],
                              cleanup_symlinks=False, overwrite=False)
    h.init()


@click.group()
@click.option('--cleanup/--no-cleanup', default=True, is_flag=True,
              help='removes broken symlinks')
@click.option('--overwrite/--no-overwrite', default=True, is_flag=True,
              help='overwrite existing files or symlinks')
@click.option('--config-path', default=None, help='path to config file')
@click.pass_context
def main(ctx, cleanup, config_path, overwrite):
    ctx.obj = {
        'cleanup': cleanup,
        'config_path': config_path,
        'overwrite': overwrite
    }


main.add_command(clean)
main.add_command(init)
