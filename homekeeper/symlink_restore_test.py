import homekeeper.config
import homekeeper.lib
import homekeeper.symlink
import homekeeper.testing

lib = homekeeper.lib
symlink = homekeeper.symlink
BaseFakeFilesystemTest = homekeeper.testing.BaseFakeFilesystemTest
ConfigData = homekeeper.config.ConfigData


class SymlinkRestoreTest(BaseFakeFilesystemTest):
    def test_restore_symlink_with_file(self, os):
        source, target = self.setup_file_symlink('.bashrc')
        symlink.restore_symlink(source, target)
        assert not os.path.islink(target)
        assert os.path.isfile(target)

    def test_restore_symlink_with_unlinked_target(self, os):
        source, target = self.setup_file_symlink('.bashrc')
        os.unlink(target)
        symlink.restore_symlink(source, target)
        assert os.path.exists(source)
        assert not os.path.exists(target)

    def test_restore_symlink_with_same_source_and_target(self, os):
        source, target = self.setup_file_symlink('.bashrc')
        symlink.restore_symlink(target, target)
        assert os.path.islink(target)
        assert source == os.readlink(target)

    def test_restore_symlink_with_directory(self, os):
        source, target = self.setup_directory_symlink('.vim')
        lib.touch(source, 'autoload', 'pathogen.vim')
        symlink.create_symlink(source, target, overwrite=True)
        symlink.restore_symlink(source, target)
        assert not os.path.islink(target)
        assert os.path.isdir(target)
        assert os.path.isfile(os.path.join(target, 'autoload', 'pathogen.vim'))

    def test_restore_symlinks(self, os, files, directories):
        config_data = ConfigData()
        config_data.excludes = []
        symlink.create_symlinks(self.dotfiles_directory, self.home_directory, config_data=config_data, overwrite=True)
        symlink.restore_symlinks(self.dotfiles_directory, self.home_directory, config_data=config_data)
        for pathname in files + directories:
            source = os.path.join(self.dotfiles_directory, pathname)
            target = os.path.join(self.home_directory, pathname)
            assert os.path.exists(source)
            assert os.path.exists(target)
            assert not os.path.islink(source)
            assert not os.path.islink(target)

    def test_restore_symlinks_with_deleted_targets(self, os, files, directories):
        config_data = ConfigData()
        config_data.excludes = []
        symlink.create_symlinks(self.dotfiles_directory, self.home_directory, config_data=config_data, overwrite=True)
        for pathname in files + directories:
            lib.remove(self.home_directory, pathname)
        symlink.restore_symlinks(self.dotfiles_directory, self.home_directory, config_data=config_data)
        for pathname in files + directories:
            source = os.path.join(self.dotfiles_directory, pathname)
            target = os.path.join(self.home_directory, pathname)
            assert os.path.exists(source)
            assert not os.path.exists(target)
