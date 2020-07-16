import logging
import homekeeper.config
import homekeeper.lib
import homekeeper.symlink


__version__ = '5.0.5'
config = homekeeper.config
lib = homekeeper.lib
symlink = homekeeper.symlink
ConfigData = homekeeper.config.ConfigData


class Homekeeper:
    def __init__(self, ctx):
        self.overwrite = ctx['overwrite']
        self.cleanup_symlinks = ctx['cleanup_symlinks']
        self.config_path = ctx['config_path']
        logging.debug("read context: %s", ctx)

    def cleanup(self):
        logging.debug('beginning cleanup')
        symlink.cleanup_symlinks(lib.get_home_directory())
        logging.debug('finished cleanup')

    def keep(self):
        logging.debug('beginning keep')
        config_data = config.read(self.config_path)
        for directory in config_data.directories:
            symlink.create_symlinks(
                directory,
                lib.get_home_directory(),
                config_data=config_data,
                overwrite=self.overwrite)
        if self.cleanup_symlinks:
            self.cleanup()
        logging.debug('finished keep')

    def unkeep(self):
        logging.debug('beginning unkeep')
        config_data = config.read(self.config_path)
        for directory in config_data.directories:
            symlink.restore_symlinks(
                directory,
                lib.get_home_directory(),
                config_data=config_data)
        if self.cleanup_symlinks:
            self.cleanup()
        logging.debug('finished unkeep')

    def version(self):
        return __version__
