import homekeeper.lib
import homekeeper.symlink
import homekeeper.testing

config = homekeeper.config
lib = homekeeper.lib
symlink = homekeeper.symlink
BaseFakeFilesystemTest = homekeeper.testing.BaseFakeFilesystemTest
ConfigData = homekeeper.config.ConfigData


class SymlinkCreateTest(BaseFakeFilesystemTest):
    def test_create_symlink_with_file(self, os):
        source = os.path.join(self.dotfiles_directory, '.bashrc')
        target = os.path.join(self.home_directory, '.bashrc')
        symlink.create_symlink(source, target)
        assert os.path.exists(target)
        assert os.readlink(target) == source

    def test_create_symlink_with_file_overwrites_target(self, os):
        source = os.path.join(self.dotfiles_directory, '.bashrc')
        target = os.path.join(self.home_directory, '.bashrc')
        symlink.create_symlink(source, target)
        source = os.path.join(self.dotfiles_directory, '.bash_profile')
        lib.touch(source)
        symlink.create_symlink(source, target, overwrite=True)
        assert os.readlink(target) == source

    def test_create_symlink__with_file_does_not_overwrite_target(self, os):
        source = os.path.join(self.dotfiles_directory, '.bashrc')
        target = os.path.join(self.home_directory, '.bashrc')
        lib.touch(source)
        symlink.create_symlink(source, target)
        source = os.path.join(self.dotfiles_directory, '.bash_profile')
        lib.touch(source)
        symlink.create_symlink(source, target, overwrite=False)
        assert os.readlink(target) != source

    def test_create_symlink_with_file_that_does_not_exist(self, os):
        source = os.path.join(self.dotfiles_directory, '.bashrc')
        target = os.path.join(self.home_directory, '.bashrc')
        lib.remove(source)
        assert not os.path.exists(source)
        assert not os.path.islink(target)

    def test_create_symlink_with_same_source_and_target(self, os):
        source = os.path.join(self.dotfiles_directory, '.bashrc')
        target = os.path.join(self.dotfiles_directory, '.bashrc')
        symlink.create_symlink(source, target)
        assert os.path.exists(source)
        assert os.path.exists(target)
        assert not os.path.islink(target)

    def test_create_symlink_with_directory(self, os):
        source = os.path.join(self.dotfiles_directory, '.vim')
        target = os.path.join(self.home_directory, '.vim')
        symlink.create_symlink(source, target)
        assert os.path.islink(target)
        assert os.readlink(target) == source

    def test_create_symlink_with_symlink(self, os):
        source = os.path.join(self.dotfiles_directory, '.vimrc.symlink')
        target = os.path.join(self.home_directory, '.vimrc')
        symlink.create_symlink(source, target)
        assert os.path.islink(target)
        assert os.readlink(target) == source

    def test_create_symlinks(self, os, files, directories):
        config_data = ConfigData()
        symlink.create_symlinks(self.dotfiles_directory, self.home_directory, config_data=config_data, overwrite=True)
        for pathname in files + directories:
            source = os.path.join(self.dotfiles_directory, pathname)
            target = os.path.join(self.home_directory, pathname)
            if pathname not in config_data.excludes:
                assert os.path.exists(source)
                assert os.path.exists(target)
                assert os.readlink(target) == source
            elif os.path.exists(source):
                assert not os.path.exists(target)

    def test_create_symlinks_does_not_overwrite(self, os, files, directories):
        for filename in files:
            lib.touch(self.home_directory, filename)
        for dirname in directories:
            lib.makedirs(self.home_directory, dirname)
        config_data = ConfigData()
        symlink.create_symlinks(self.dotfiles_directory, self.home_directory, config_data=config_data, overwrite=False)
        for pathname in files + directories:
            source = os.path.join(self.dotfiles_directory, pathname)
            target = os.path.join(self.home_directory, pathname)
            assert os.path.exists(source)
            assert os.path.exists(target)
            assert not os.path.islink(target)

    def test_create_symlinks_excludes_paths(self, os, files, directories):
        config_data = ConfigData()
        config_data.excludes = files + directories
        symlink.create_symlinks(self.dotfiles_directory, self.home_directory, config_data=config_data, overwrite=True)
        for pathname in files + directories:
            source = os.path.join(self.dotfiles_directory, pathname)
            target = os.path.join(self.home_directory, pathname)
            assert os.path.exists(source)
            assert not os.path.exists(target)
