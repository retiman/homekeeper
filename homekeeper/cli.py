import click
import homekeeper
import logging


@click.command(short_help='Removes broken symlinks only.')
@click.pass_context
def cleanup(ctx):
    h = ctx.obj['homekeeper']
    h.cleanup_symlinks = True
    h.overwrite = False
    h.cleanup()


@click.command(short_help='Set dotfiles directory to current directory.')
@click.pass_context
def init(ctx):
    h = ctx.obj['homekeeper']
    h.cleanup_symlinks = False
    h.overwrite = False
    h.cleanup()


@click.command(short_help='Symlinks dotfiles to your home directory.')
@click.pass_context
def keep(ctx):
    h = ctx.obj['homekeeper']
    h.keep()


@click.command(short_help='Restores dotfiles and replacing symlinks.')
@click.pass_context
def unkeep(ctx):
    h = ctx.obj['homekeeper']
    h.unkeep()


@click.group()
@click.option('--cleanup-symlinks/--no-cleanup-symlinks', default=True,
              is_flag=True, help='Removes broken symlinks (default true).')
@click.option('--overwrite/--no-overwrite', default=True, is_flag=True,
              help='Overwrite existing files or symlinks (default true).')
@click.option('--config-path', metavar='FILE', default=None,
              help='Path to .homekeeper.json config file.')
@click.option('--debug/--no-debug', default=False, is_flag=True,
              help='Enables debug output (default false).')
@click.pass_context
def main(ctx, cleanup_symlinks, config_path, overwrite, debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(message)s', level=logging.INFO)
    h = homekeeper.Homekeeper(config_path=config_path)
    h.cleanup_symlinks = cleanup_symlinks
    h.overwrite = overwrite
    ctx.obj = dict()
    ctx.obj['config_path'] = config_path
    ctx.obj['homekeeper'] = h


main.add_command(cleanup)
main.add_command(init)
main.add_command(keep)
main.add_command(unkeep)
