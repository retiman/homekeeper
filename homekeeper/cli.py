import logging
import sys
import click
import homekeeper
import homekeeper.exceptions


ConfigException = homekeeper.exceptions.ConfigException
Homekeeper = homekeeper.Homekeeper
HomekeeperException = homekeeper.exceptions.HomekeeperException


@click.command(short_help='removes broken symlinks only')
@click.pass_context
def cleanup(ctx):
    try:
        h = Homekeeper(ctx.obj)
        if not h.cleanup_symlinks:
            logging.warning('read flag --no-cleanup-symlinks but forcing value to be true')
            h.cleanup_symlinks = True
        h.cleanup()
    except (ConfigException, HomekeeperException) as e:
        logging.error(e)
        sys.exit(1)


@click.command(short_help='symlinks dotfiles to your home directory')
@click.pass_context
def keep(ctx):
    try:
        h = Homekeeper(ctx.obj)
        h.keep()
    except (ConfigException, HomekeeperException) as e:
        logging.error(e)
        sys.exit(1)


@click.command(short_help='restores dotfiles and replacing symlinks')
@click.pass_context
def unkeep(ctx):
    try:
        h = Homekeeper(ctx.obj)
        h.unkeep()
    except (ConfigException, HomekeeperException) as e:
        logging.error(e)
        sys.exit(1)


@click.command(short_help='displays the version and then exits')
@click.pass_context
def version(ctx):
    try:
        h = Homekeeper(ctx.obj)
        click.echo('homekeeper version %s' % h.version())
    except (ConfigException, HomekeeperException) as e:
        logging.error(e)
        sys.exit(1)


@click.group()
@click.option('--cleanup-symlinks/--no-cleanup-symlinks',
              default=True,
              is_flag=True,
              help='removes broken symlinks (default true)')
@click.option('--overwrite/--no-overwrite',
              default=True,
              is_flag=True,
              help='overwrite existing files or symlinks (default true)')
@click.option('--config-path',
              metavar='FILE',
              default=None,
              help='path to .homekeeper.json config file')
@click.option('--debug/--no-debug',
              default=False,
              is_flag=True,
              help='enables debug output (default false)')
@click.pass_context
def main(ctx, cleanup_symlinks, overwrite, config_path, debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.info('set log level to debug')
    else:
        logging.basicConfig(format='%(message)s', level=logging.INFO)
    ctx.obj = {
        'cleanup_symlinks': cleanup_symlinks,
        'config_path': config_path,
        'overwrite': overwrite,
    }
    logging.debug("created click context object: %s", ctx.obj)


main.add_command(cleanup)
main.add_command(keep)
main.add_command(unkeep)
main.add_command(version)
