import homekeeper
import homekeeper.common
import homekeeper.config
import homekeeper.test_case
import json

cd = homekeeper.common.cd

# pylint: disable=attribute-defined-outside-init
# pylint: disable=no-self-use
class TestHomekeeper(homekeeper.test_case.TestCase):
    def setup_method(self):
        super(TestHomekeeper, self).setup_method()
        self.patch('homekeeper')
        self.patch('homekeeper.common')
        self.patch('homekeeper.config')
        self.patch('homekeeper.core')
        self.setup_files()

    def setup_files(self):
        with cd(self.base_directory):
            self.setup_file('.bash_aliases', data='base')
            self.setup_file('.bash_local', data='base')
            self.setup_file('.bash_profile')
            self.setup_file('.git')
            self.setup_file('.gitconfig')
            self.setup_file('.gitignore')
            self.setup_file('.vimrc')
            self.setup_directory('.tmux')
            self.setup_directory('.tmux', 'base')
            self.setup_directory('.tmuxp')
            self.setup_directory('.tmuxp', 'base')
            self.setup_directory('.vim')
        with cd(self.dotfiles_directory):
            self.setup_file('.bash_aliases', data='dotfiles')
            self.setup_file('.bash_local', data='dotfiles')
            self.setup_file('.xbindkeysrc', data='dotfiles')
            self.setup_directory('.tmux')
            self.setup_directory('.tmuxp')
            self.setup_directory('bin')
        with cd(self.custom_directory):
            self.setup_directory('base')
            self.setup_directory('dotfiles')

    def test_setters_override_config(self):
        h = homekeeper.Homekeeper()
        assert h.config.overwrite
        assert h.config.cleanup_symlinks
        h.overwrite = False
        h.cleanup_symlinks = False
        assert not h.config.overwrite
        assert not h.config.cleanup_symlinks

    def test_init_saves_config(self, os):
        with cd(self.custom_directory):
            config = os.path.join(self.custom_directory, '.homekeeper.json')
            homekeeper.Homekeeper(config_path=config).init()
            data = json.loads(self.read_file(config))
            assert self.custom_directory == data['dotfiles_directory']

    def test_init_with_default_config_path(self):
        h = homekeeper.Homekeeper()
        assert h.config.base_directory == self.base_directory
        assert h.config.dotfiles_directory == self.dotfiles_directory
        assert '.git' in h.config.excludes

    def test_keep_overrides_base_files(self, os):
        h = homekeeper.Homekeeper()
        h.keep()
        base_items = set(os.listdir(self.base_directory))
        dotfiles_items = set(os.listdir(self.dotfiles_directory))
        for item in os.listdir(self.home):
            assert item not in h.config.excludes
            if item not in base_items and item not in dotfiles_items:
                continue
            link = os.path.join(self.home, item)
            target_directory = (self.dotfiles_directory if
                                item in dotfiles_items else self.base_directory)
            assert os.path.islink(link)
            assert os.path.join(target_directory, item) == os.readlink(link)

    def test_unkeep_restores_files(self, os):
        self.setup_file(self.home, '.unrelatedrc')
        os.symlink(os.path.join(self.home, '.unrelatedrc'),
                   os.path.join(self.home, '.link-to-unrelatedrc'))
        os.symlink(os.path.join(self.base_directory, '.vimrc'),
                   os.path.join(self.home, '.vimrc'))
        os.symlink(os.path.join(self.base_directory, '.vim'),
                   os.path.join(self.home, '.vim'))
        os.symlink(os.path.join(self.dotfiles_directory, '.bash_local'),
                   os.path.join(self.home, '.bash_local'))
        os.symlink(os.path.join(self.dotfiles_directory, '.tmux'),
                   os.path.join(self.home, '.tmux'))
        h = homekeeper.Homekeeper()
        h.unkeep()
        assert os.path.exists(os.path.join(self.home, '.unrelatedrc'))
        assert os.path.islink(os.path.join(self.home, '.link-to-unrelatedrc'))
        assert not os.path.islink(os.path.join(self.home, '.unrelatedrc'))
        assert not os.path.islink(os.path.join(self.home, '.tmux'))
        assert not os.path.islink(os.path.join(self.home, '.vim'))
        assert not os.path.islink(os.path.join(self.home, '.bash_local'))
        assert not os.path.islink(os.path.join(self.home, '.vimrc'))
        assert 'dotfiles' == self.read_file(self.home, '.bash_local')

    def test_cleanup_symlinks(self, os):
        self.setup_file(self.home, '.missingrc')
        os.symlink(os.path.join(self.home, '.missingrc'),
                   os.path.join(self.home, '.brokenrc'))
        os.unlink(os.path.join(self.home, '.missingrc'))
        os.symlink(os.path.join(self.base_directory, '.vimrc'),
                   os.path.join(self.home, '.vimrc'))
        assert os.path.islink(os.path.join(self.home, '.brokenrc'))
        assert os.path.islink(os.path.join(self.home, '.vimrc'))
        h = homekeeper.Homekeeper()
        h.cleanup_symlinks = True
        h.cleanup()
        assert not os.path.exists(os.path.join(self.home, '.brokenrc'))
        assert os.path.islink(os.path.join(self.home, '.vimrc'))
