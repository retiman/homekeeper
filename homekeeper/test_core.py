import homekeeper.common
import homekeeper.core
import homekeeper.test_case

cd = homekeeper.common.cd


# pylint: disable=attribute-defined-outside-init
# pylint: disable=too-many-public-methods
class TestCore(homekeeper.test_case.TestCase):
    def setup_method(self):
        super(TestCore, self).setup_method()
        self.patch('homekeeper.common')
        self.patch('homekeeper.core')

    def setup_symlink(self, os):
        source = self.setup_file(self.dotfiles_directory, '.vimrc')
        target = os.path.join(self.home, '.vimrc')
        return source, target

    def verify_symlink(self, os, source, target): # pylint: disable=no-self-use
        assert os.path.exists(source)
        assert os.path.exists(target)
        assert os.path.islink(target)
        assert source == os.readlink(target)
        if os.path.isfile(source):
            assert os.path.isfile(target)
        if os.path.isdir(source):
            assert os.path.isdir(target)

    def test_symlink_with_no_target(self, os):
        source, target = self.setup_symlink(os)
        homekeeper.core.symlink(source, target)
        self.verify_symlink(os, source, target)

    def test_symlink_with_file_target(self, os):
        source, target = self.setup_symlink(os)
        self.setup_file(target)
        homekeeper.core.symlink(source, target, overwrite=True)
        self.verify_symlink(os, source, target)

    def test_symlink_with_directory_target(self, os):
        source, target = self.setup_symlink(os)
        self.setup_directory(os.path.dirname(target))
        homekeeper.core.symlink(source, target, overwrite=True)
        self.verify_symlink(os, source, target)

    def test_symlink_with_symlink_target(self, os):
        source, target = self.setup_symlink(os)
        original_source = self.setup_file(self.home, 'vimrc')
        os.symlink(original_source, target)
        homekeeper.core.symlink(source, target, overwrite=True)
        self.verify_symlink(os, source, target)

    def test_symlink_with_no_overwrite(self, os):
        source, target = self.setup_symlink(os)
        self.setup_file(target)
        homekeeper.core.symlink(source, target, overwrite=False)
        assert os.path.exists(source)
        assert os.path.exists(target)
        assert not os.path.islink(target)

    def test_symlink_with_same_source_and_target(self, os):
        source, target = self.setup_symlink(os)
        homekeeper.core.symlink(source, source, overwrite=True)
        assert not os.path.exists(target)
        assert not os.path.islink(source)

    def test_restore_file_symlink(self, os):
        source, target = self.setup_symlink(os)
        homekeeper.core.symlink(source, target, overwrite=True)
        homekeeper.core.restore(source, target, overwrite=True)
        assert not os.path.islink(target)
        assert os.path.isfile(target)

    def test_restore_directory_symlink(self, os):
        source = os.path.join(self.dotfiles_directory, '.vim')
        target = os.path.join(self.home, '.vim')
        self.setup_file(source, '.vim', 'autoload', 'pathogen.vim')
        homekeeper.core.symlink(source, target, overwrite=True)
        homekeeper.core.restore(source, target, overwrite=True)
        assert not os.path.islink(target)
        assert os.path.isdir(target)
        assert os.path.isfile(os.path.join(target, '.vim', 'autoload',
                                           'pathogen.vim'))

    def test_restore_symlink_with_no_target(self, os):
        source, target = self.setup_symlink(os)
        homekeeper.core.symlink(source, target, overwrite=True)
        os.unlink(target)
        homekeeper.core.restore(source, target, overwrite=False)
        assert not os.path.exists(target)

    def test_restore_symlink_with_same_source_and_target(self, os):
        source, target = self.setup_symlink(os)
        homekeeper.core.symlink(source, target, overwrite=True)
        homekeeper.core.restore(target, target, overwrite=True)
        assert os.path.islink(target)
        assert source == os.readlink(target)

    def test_create_symlinks(self, os):
        source, target = self.setup_symlink(os)
        source_directory = os.path.dirname(source)
        assert os.path.exists(source)
        assert not os.path.exists(target)
        homekeeper.core.create_symlinks(source_directory, self.home,
                                        overwrite=True)
        self.verify_symlink(os, source, target)

    def test_create_symlinks_with_same_source_and_target(self, os):
        homekeeper.core.create_symlinks(self.home, self.home)
        for item in os.listdir(self.home):
            assert not os.path.islink(os.path.join(self.home, item))

    def test_create_symlinks_with_no_source_directory(self, os):
        self.setup_directory(self.home)
        source_directory = os.path.join(self.home, 'non-existant-directory')
        homekeeper.core.create_symlinks(source_directory, self.home,
                                        overwrite=True)
        for item in os.listdir(self.home):
            assert not os.path.islink(item)

    def test_create_symlinks_with_no_overwrite(self, os):
        source, target = self.setup_symlink(os)
        source_directory = os.path.dirname(source)
        self.setup_file(target)
        homekeeper.core.create_symlinks(source_directory, self.home,
                                        overwrite=False)
        assert os.path.exists(source)
        assert os.path.exists(target)
        assert not os.path.islink(target)

    def test_create_symlinks_with_multiple_sources(self, os):
        source_files = ['.bash_profile', '.gitignore', '.gvimrc', '.vimrc']
        source_directories = ['bin', '.git', '.vim']
        excludes = ['.git', '.gitignore']
        for item in source_files:
            self.setup_file(self.dotfiles_directory, item)
            self.setup_file(self.home, item)
        for item in source_directories:
            self.setup_directory(self.dotfiles_directory, item)
            self.setup_file(self.home, item)
        homekeeper.core.create_symlinks(self.dotfiles_directory, self.home,
                                        excludes=excludes, overwrite=True)
        for item in source_files:
            if item in excludes:
                assert not os.path.islink(os.path.join(self.home, item))
            else:
                source = os.path.join(self.dotfiles_directory, item)
                target = os.path.join(self.home, item)
                self.verify_symlink(os, source, target)

    def test_cleanup_symlinks(self, os):
        with cd(self.home):
            self.setup_file('existing.txt')
            os.symlink('existing.txt', 'existing-link.txt')
            os.symlink('non-existing-1.txt', 'non-existing-1-link.txt')
            os.symlink('non-existing-2.txt', 'non-existing-2-link.txt')
            homekeeper.core.cleanup_symlinks(self.home)
            assert os.path.exists('existing.txt')
            assert os.path.exists('existing-link.txt')
            assert not os.path.exists('non-existing-1-link.txt')
            assert not os.path.exists('non-existing-2-link.txt')
