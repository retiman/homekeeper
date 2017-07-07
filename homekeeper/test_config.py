import homekeeper.config
import homekeeper.test_case
import json


# pylint: disable=attribute-defined-outside-init
class TestConfig(homekeeper.test_case.TestCase):
    def setup_method(self):
        super(TestConfig, self).setup_method()
        self.patch('homekeeper.common')
        self.patch('homekeeper.config')
        self.config = homekeeper.config.Config()
        self.config_path = self.fake_os.path.join(self.home, '.homekeeper.json')

    def test_load(self, os):
        self.config.load(self.config_path)
        excludes = ['.git', '.gitignore']
        includes = [os.path.join(self.home, '.foo', 'foorc')]
        assert self.base_directory == self.config.base_directory
        assert self.dotfiles_directory == self.config.dotfiles_directory
        assert excludes == self.config.excludes
        assert includes == self.config.includes
        assert self.config.override

    def test_load_with_defaults(self):
        self.setup_file(self.config_path, data=json.dumps({}))
        self.config.load(self.config_path)
        assert not self.config.base_directory
        assert self.dotfiles_directory == self.config.dotfiles_directory
        assert [] == self.config.excludes
        assert [] == self.config.includes
        assert not self.config.override

    def test_load_and_save_old_config(self, os):
        config_path = os.path.join(self.home, 'custom', '.homekeeper.json')
        base_directory = os.path.join(self.home, 'custom', 'base')
        dotfiles_directory = os.path.join(self.home, 'custom', 'dotfiles')
        excludes = ['.git']
        includes = [os.path.join(self.home, '.bar', 'barrc')]
        self.config.load(config_path)
        assert base_directory == self.config.base_directory
        assert dotfiles_directory == self.config.dotfiles_directory
        assert excludes == self.config.excludes
        assert includes == self.config.includes
        assert self.config.override
        self.config.save(config_path)
        data = json.loads(self.read_file(config_path))
        assert data['base_directory'] == base_directory
        assert data['dotfiles_directory'] == dotfiles_directory
        assert data['excludes'] == excludes
        assert data['includes'] == includes
        assert 'override' not in data
        assert 'cherrypicks' not in data
        assert 'base' not in data
        assert 'directory' not in data

    def test_save(self, os):
        self.setup_directory(os.path.dirname(self.config_path))
        self.config.base_directory = None
        self.config.dotfiles_directory = os.path.join(self.home, 'custom')
        self.config.excludes = ['.idea']
        self.config.override = False
        self.config.save(self.config_path)
        data = json.loads(self.read_file(self.config_path))
        assert data['base_directory'] == self.config.base_directory
        assert data['dotfiles_directory'] == self.config.dotfiles_directory
        assert data['excludes'] == self.config.excludes
        assert 'override' not in data
        assert 'cherrypicks' not in data
        assert 'base' not in data
        assert 'directory' not in data
