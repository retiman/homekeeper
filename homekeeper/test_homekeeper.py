import homekeeper
import homekeeper.config
import homekeeper.test_case
import json

from homekeeper.common import makedirs

os = None


class TestHomekeeper(homekeeper.test_case.TestCase):
    def setup_method(self):
        super(TestHomekeeper, self).setup_method()
        self.setup_filesystem()
        self.patch('homekeeper')
        self.patch('homekeeper.common')
        self.patch('homekeeper.config')
        self.patch('homekeeper.main')
        self.setup_base_directory()
        self.setup_dotfiles_directory()
        self.setup_homekeeper_json()
        os.chdir(os.getenv('HOME'))

    def setup_filesystem(self):
        global os
        os = self.os

    def setup_homekeeper_json(self):
        base_directory = self.home('custom_base')
        dotfiles_directory = self.home('custom_dotfiles')
        excludes = ['.git']
        data = {
            'base_directory': base_directory,
            'dotfiles_directory': dotfiles_directory,
            'excludes': excludes
        }
        self.custom_homekeeper_json = self.home('custom', '.homekeeper.json')
        self.write_homekeeper_json(self.custom_homekeeper_json, data)
        self.homekeeper_json = self.home('.homekeeper.json')
        data['base_directory'] = self.base_directory
        data['dotfiles_directory'] = self.dotfiles_directory
        self.write_homekeeper_json(self.homekeeper_json, data)

    def setup_base_directory(self):
        self.base_directory = self.home('dotfiles', 'base')
        makedirs(self.base_directory)
        self.files = [
            '.bash_aliases',
            '.bash_local',
            '.bash_profile',
            '.git',
            '.gitconfig',
            '.gitignore',
        ]
        self.directories = [
            '.tmux',
            '.tmuxp',
            '.vim',
        ]
        for filename in self.files:
            self.touch(self.base_directory, filename)
        for dirname in self.directories:
            makedirs(self.path(self.base_directory, dirname))
        bash_local = self.path(self.base_directory, '.bash_local')
        with self.fopen(bash_local, 'w') as f:
            f.write('export BASE_DIRECTORY=1')

    def setup_dotfiles_directory(self):
        self.dotfiles_directory = self.home('dotfiles', 'main')
        makedirs(self.dotfiles_directory)
        bash_local = self.path(self.dotfiles_directory, '.bash_local')
        with self.fopen(bash_local, 'w') as f:
            f.write('export DOTFILES_DIRECTORY=1')
        self.touch(self.dotfiles_directory, '.bash_aliases')
        makedirs(self.path(self.dotfiles_directory, '.tmux'))

    def write_homekeeper_json(self, pathname, data):
        self.touch(pathname)
        with self.fopen(pathname, 'w') as f:
            f.write(json.dumps(data))

    def test_init_saves_config(self):
        custom_dotfiles_directory = self.path(os.sep, 'custom')
        makedirs(custom_dotfiles_directory)
        os.chdir(custom_dotfiles_directory)
        h = homekeeper.Homekeeper(pathname=self.custom_homekeeper_json)
        h.init()
        with self.fopen(self.custom_homekeeper_json, 'r') as f:
            data = json.loads(f.read())
        assert custom_dotfiles_directory == data['dotfiles_directory']

    def test_init_with_default_config_path(self):
        h = homekeeper.Homekeeper()
        assert h.config.base_directory == self.base_directory
        assert h.config.dotfiles_directory == self.dotfiles_directory
        assert '.git' in h.config.excludes
