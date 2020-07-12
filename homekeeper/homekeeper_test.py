import pytest
import homekeeper.lib
import homekeeper.testing


cd = homekeeper.lib.cd
config = homekeeper.config
lib = homekeeper.lib
BaseFakeFilesystemTest = homekeeper.testing.BaseFakeFilesystemTest
ConfigData = homekeeper.config.ConfigData
Homekeeper = homekeeper.Homekeeper


class HomekeeperTest(BaseFakeFilesystemTest):
    @pytest.fixture
    def ctx(self):
        return {
            'cleanup_symlinks': True,
            'config_path': '',
            'overwrite': True,
        }

    # pylint: disable=unused-argument
    def test_simple_usage(self, ctx, os, files, directories):
        config_data = ConfigData()
        config_data.directories = [os.path.join(lib.get_home_directory(), 'dotfiles')]
        config_file = config.write(config_data)
        assert os.path.exists(config_file)
        h = Homekeeper(ctx)
        h.keep()
        h.unkeep()
        h.cleanup()
        assert h.version() == homekeeper.__version__
        for pathname in os.listdir(lib.get_home_directory()):
            assert not os.path.islink(pathname)
