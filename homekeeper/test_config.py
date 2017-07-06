import homekeeper.config
import homekeeper.test_case
import json

from homekeeper.common import makedirs

os = None


class TestConfig(homekeeper.test_case.TestCase):
    def setup_method(self):
        super(TestConfig, self).setup_method()
        self.setup_filesystem()
        self.patch('homekeeper.common')
        self.patch('homekeeper.config')
        self.config = homekeeper.config.Config()
        self.config_path = self.path(self.home(), '.homekeeper.json')

    def setup_filesystem(self):
        global os
        os = self.os

    def test_load(self):
        base_directory = self.path(self.home(), 'base')
        dotfiles_directory = self.path(self.home(), 'dotfiles')
        excludes = ['.git']
        data = {
            'base_directory': base_directory,
            'dotfiles_directory': dotfiles_directory,
            'excludes': excludes
        }
        self.fs.CreateFile(self.config_path, contents=json.dumps(data))
        self.config.load(self.config_path)
        assert base_directory == self.config.base_directory
        assert dotfiles_directory == self.config.dotfiles_directory
        assert excludes == self.config.excludes
        assert self.config.override

    def test_load_with_defaults(self):
        dotfiles_directory = self.path(self.home(), 'dotfiles')
        self.fs.CreateFile(self.config_path, contents=json.dumps({}))
        self.config.load(self.config_path)
        assert not self.config.base_directory
        assert dotfiles_directory == self.config.dotfiles_directory
        assert [] == self.config.excludes
        assert not self.config.override

    def test_save(self):
        makedirs(os.path.dirname(self.config_path))
        self.config.base_directory = None
        self.config.dotfiles_directory = self.path(self.home(), 'dotfiles2')
        self.config.excludes = ['.idea']
        self.config.override = False
        self.config.save(self.config_path)
        with self.fopen(self.config_path, 'r') as f:
            data = json.loads(f.read())
            assert data['base_directory'] == self.config.base_directory
            assert data['dotfiles_directory'] == self.config.dotfiles_directory
            assert data['excludes'] == self.config.excludes
            assert 'override' not in data
