import click
import homekeeper
import logging


@click.command(short_help='Removes broken symlinks only.')
@click.pass_context
def cleanup(ctx):
    h = create_homekeeper(ctx.obj)
    h.cleanup_symlinks = True
    h.overwrite = False
    h.cleanup()


@click.command(short_help='Set dotfiles directory to current directory.')
@click.pass_context
def init(ctx):
    h = create_homekeeper(ctx.obj)
    h.cleanup_symlinks = False
    h.overwrite = False
    h.cleanup()


@click.command(short_help='Symlinks dotfiles to your home directory.')
@click.pass_context
def keep(ctx):
    h = create_homekeeper(ctx.obj)
    h.keep()


@click.command(short_help='Restores dotfiles and replacing symlinks.')
@click.pass_context
def unkeep(ctx):
    h = create_homekeeper(ctx.obj)
    h.unkeep()


@click.command(short_help='Displays the version and then exits.')
@click.pass_context
def version(ctx): # pylint: disable=unused-argument
    click.echo('Homekeeper version %s' % homekeeper.__version__)


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
def main(ctx, cleanup_symlinks, overwrite, config_path, debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(message)s', level=logging.INFO)
    ctx.obj = {
        'cleanup_symlinks': cleanup_symlinks,
        'config_path': config_path,
        'overwrite': overwrite,
    }


def create_homekeeper(args):
    h = homekeeper.Homekeeper(config_path=args['config_path'])
    h.cleanup_symlinks = args['cleanup_symlinks']
    h.overwrite = args['overwrite']
    return h


main.add_command(cleanup)
main.add_command(init)
main.add_command(keep)
main.add_command(unkeep)
main.add_command(version)
