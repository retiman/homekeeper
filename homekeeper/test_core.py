import homekeeper.common
import homekeeper.config
import homekeeper.core
import homekeeper.test_case

cd = homekeeper.common.cd
core = homekeeper.core


# pylint: disable=attribute-defined-outside-init
# pylint: disable=no-self-use
# pylint: disable=too-many-public-methods
class TestCore(homekeeper.test_case.TestCase):
    def setup_method(self):
        super(TestCore, self).setup_method()
        self.patch('homekeeper.common')
        self.patch('homekeeper.core')
        self.config = homekeeper.config.Config()

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

    def test_directory_symlinks(self, os):
        source = self.setup_directory(self.dotfiles_directory, '.vim')
        target = self.setup_directory(self.home, '.vim')
        core.symlink(self.config, source, target)
        self.verify_symlink(os, source, target)

    def test_symlink_with_no_target(self, os):
        source, target = self.setup_symlink(os)
        core.symlink(self.config, source, target)
        self.verify_symlink(os, source, target)

    def test_symlink_with_file_target(self, os):
        source, target = self.setup_symlink(os)
        self.setup_file(target)
        self.config.overwrite = True
        core.symlink(self.config, source, target)
        self.verify_symlink(os, source, target)

    def test_symlink_with_directory_target(self, os):
        source, target = self.setup_symlink(os)
        self.setup_directory(os.path.dirname(target))
        self.config.overwrite = True
        core.symlink(self.config, source, target)
        self.verify_symlink(os, source, target)

    def test_symlink_with_symlink_target(self, os):
        source, target = self.setup_symlink(os)
        original_source = self.setup_file(self.home, 'vimrc')
        os.symlink(original_source, target)
        self.config.overwrite = True
        core.symlink(self.config, source, target)
        self.verify_symlink(os, source, target)

    def test_symlink_with_no_overwrite(self, os):
        source, target = self.setup_symlink(os)
        self.setup_file(target)
        self.config.overwrite = False
        core.symlink(self.config, source, target)
        assert os.path.exists(source)
        assert os.path.exists(target)
        assert not os.path.islink(target)

    def test_symlink_with_same_source_and_target(self, os):
        source, target = self.setup_symlink(os)
        self.config.overwrite = True
        core.symlink(self.config, source, source)
        assert not os.path.exists(target)
        assert not os.path.islink(source)

    def test_restore_file_symlink(self, os):
        source, target = self.setup_symlink(os)
        core.symlink(self.config, source, target)
        core.restore(self.config, source, target)
        assert not os.path.islink(target)
        assert os.path.isfile(target)

    def test_restore_directory_symlink(self, os):
        source = os.path.join(self.dotfiles_directory, '.vim')
        target = os.path.join(self.home, '.vim')
        self.setup_file(source, '.vim', 'autoload', 'pathogen.vim')
        core.symlink(self.config, source, target)
        core.restore(self.config, source, target)
        assert not os.path.islink(target)
        assert os.path.isdir(target)
        assert os.path.isfile(os.path.join(target, '.vim', 'autoload',
                                           'pathogen.vim'))

    def test_restore_symlink_with_no_target(self, os):
        source, target = self.setup_symlink(os)
        core.symlink(self.config, source, target)
        os.unlink(target)
        core.restore(self.config, source, target)
        assert os.path.exists(source)
        assert not os.path.exists(target)

    def test_restore_symlink_with_same_source_and_target(self, os):
        source, target = self.setup_symlink(os)
        core.symlink(self.config, source, target)
        core.restore(self.config, target, target)
        assert os.path.islink(target)
        assert source == os.readlink(target)

    def test_create_symlinks(self, os):
        source, target = self.setup_symlink(os)
        source_directory = os.path.dirname(source)
        assert os.path.exists(source)
        assert not os.path.exists(target)
        self.config.overwrite = True
        core.create_symlinks(self.config, source_directory, self.home)
        self.verify_symlink(os, source, target)

    def test_create_symlinks_with_same_source_and_target(self, os):
        core.create_symlinks(self.config, self.home, self.home)
        for item in os.listdir(self.home):
            assert not os.path.islink(os.path.join(self.home, item))

    def test_create_symlinks_with_no_source_directory(self, os):
        self.setup_directory(self.home)
        source_directory = os.path.join(self.home, 'non-existant-directory')
        core.create_symlinks(self.config, source_directory, self.home)
        for item in os.listdir(self.home):
            assert not os.path.islink(item)

    def test_create_symlinks_with_no_overwrite(self, os):
        source, target = self.setup_symlink(os)
        source_directory = os.path.dirname(source)
        self.setup_file(target)
        self.config.overwrite = False
        core.create_symlinks(self.config, source_directory, self.home)
        assert os.path.exists(source)
        assert os.path.exists(target)
        assert not os.path.islink(target)

    def test_create_symlinks_with_multiple_sources(self, os):
        source_files = ['.bash_profile', '.gitignore', '.gvimrc', '.vimrc']
        source_directories = ['bin', '.git', '.vim']
        self.config.excludes = ['.git', '.gitignore']
        self.config.overwrite = True
        for item in source_files:
            self.setup_file(self.dotfiles_directory, item)
            self.setup_file(self.home, item)
        for item in source_directories:
            self.setup_directory(self.dotfiles_directory, item)
            self.setup_file(self.home, item)
        core.create_symlinks(self.config, self.dotfiles_directory, self.home)
        for item in source_files:
            if item in self.config.excludes:
                assert not os.path.islink(os.path.join(self.home, item))
            else:
                source = os.path.join(self.dotfiles_directory, item)
                target = os.path.join(self.home, item)
                self.verify_symlink(os, source, target)

    def test_create_symlinks_with_includes(self, os):
        include = self.setup_file(self.dotfiles_directory, '.foo', 'bar',
                                  'bazrc')
        target = os.path.join(self.home, '.foo', 'bar', 'bazrc')
        self.config.includes = [include]
        core.create_symlinks(self.config, self.dotfiles_directory, self.home)
        assert not os.path.islink(os.path.join(self.home, '.foo'))
        assert os.path.exists(target)
        assert os.path.islink(target)
        assert os.readlink(target) == include

    def test_create_symlinks_with_single_directory_includes(self, os):
        include = self.setup_file(self.dotfiles_directory, '.foo')
        target = os.path.join(self.home, '.foo')
        self.config.includes = [include]
        core.create_symlinks(self.config, self.dotfiles_directory, self.home)
        assert os.path.exists(target)
        assert os.path.islink(target)
        assert os.readlink(target) == include

    def test_create_with_bad_includes(self, os):
        self.config.includes = ['', 'non-existing', os.sep]
        core.create_symlinks(self.config, self.dotfiles_directory, self.home)
        assert not os.path.exists(os.path.join(self.dotfiles_directory,
                                               'non-existing'))

    def test_cleanup_symlinks(self, os):
        with cd(self.home):
            self.setup_file('existing.txt')
            os.symlink('existing.txt', 'existing-link.txt')
            os.symlink('non-existing-1.txt', 'non-existing-1-link.txt')
            os.symlink('non-existing-2.txt', 'non-existing-2-link.txt')
            core.cleanup_symlinks(self.home)
            assert os.path.exists('existing.txt')
            assert os.path.exists('existing-link.txt')
            assert not os.path.exists('non-existing-1-link.txt')
            assert not os.path.exists('non-existing-2-link.txt')

    def test_firstpart(self, os):
        assert core.firstpart(os.path.join(os.sep, 'foo', 'bar')) == os.sep
        assert core.firstpart(os.path.join('foo', 'bar')) == 'foo'
        assert core.firstpart('bar') == 'bar'

    def test_relativize(self, os):
        base_directory = os.path.join(os.sep, 'foo', 'bar', 'baz')
        assert core.relativize(os.path.join(base_directory, 'bif'),
                               base_directory) == 'bif'

    def test_is_valid_include(self, os):
        commonprefix = self.dotfiles_directory
        os.chdir(commonprefix)
        assert core.is_valid_include(os.sep, commonprefix) == False
        assert core.is_valid_include('foobar', commonprefix) == False
        assert core.is_valid_include('..', commonprefix) == False
        assert core.is_valid_include('.', commonprefix) == False
        self.setup_file(self.dotfiles_directory, 'foobar')
        assert core.is_valid_include('foobar', commonprefix) == True
