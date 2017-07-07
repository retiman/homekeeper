import homekeeper
import homekeeper.config
import homekeeper.test_case
import json


# pylint: disable=attribute-defined-outside-init
class TestHomekeeper(homekeeper.test_case.TestCase):
    def setup_method(self):
        super(TestHomekeeper, self).setup_method()
        self.patch('homekeeper')
        self.patch('homekeeper.common')
        self.patch('homekeeper.config')
        self.patch('homekeeper.core')
        self.setup_files(self.fake_os)
        self.setup_homekeeper_json(self.fake_os)
        self.setup_custom_homekeeper_json(self.fake_os)
        self.fake_os.chdir(self.fake_os.getenv('HOME'))

    def setup_files(self, os):
        self.base_directory = os.path.join(os.sep, 'base')
        self.dotfiles_directory = os.path.join(os.sep, 'dotfiles')
        self.custom_directory = os.path.join(os.sep, 'custom')
        self.setup_file('base', '.bash_aliases', data='base')
        self.setup_file('base', '.bash_local', data='base')
        self.setup_file('base', '.bash_profile')
        self.setup_file('base', '.git')
        self.setup_file('base', '.gitconfig')
        self.setup_file('base', '.gitignore')
        self.setup_file('base', '.vimrc')
        self.setup_file('dotfiles', '.bash_aliases', data='dotfiles')
        self.setup_file('dotfiles', '.bash_local', data='dotfiles')
        self.setup_file('dotfiles', '.xbindkeysrc', data='dotfiles')
        self.setup_directory('base', '.tmux')
        self.setup_directory('base', '.tmux', 'base')
        self.setup_directory('base', '.tmuxp')
        self.setup_directory('base', '.tmuxp', 'base')
        self.setup_directory('base', '.vim')
        self.setup_directory('custom', 'base')
        self.setup_directory('custom', 'dotfiles')
        self.setup_directory('dotfiles', '.tmux')
        self.setup_directory('dotfiles', '.tmuxp')
        self.setup_directory('dotfiles', 'bin')

    def setup_homekeeper_json(self, os):
        data = json.dumps({
            'base_directory': self.base_directory,
            'dotfiles_directory': self.dotfiles_directory,
            'excludes': ['.git', '.gitignore'],
        })
        self.setup_file(os.getenv('HOME'), '.homekeeper.json', data=data)

    def setup_custom_homekeeper_json(self, os):
        data = json.dumps({
            'base_directory': os.path.join(self.custom_directory, 'base'),
            'dotfiles_directory': os.path.join(self.custom_directory,
                                               'dotfiles'),
            'excludes': ['.git', '.gitignore'],
        })
        self.setup_file(self.custom_directory, '.homekeeper.json', data=data)

    def test_init_saves_config(self, os):
        os.chdir(self.custom_directory)
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
        for item in os.listdir(os.getenv('HOME')):
            if item in h.config.excludes:
                continue
            if item not in base_items and item not in dotfiles_items:
                continue
            link = os.path.join(os.getenv('HOME'), item)
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
