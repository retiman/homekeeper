import homekeeper
import homekeeper.common
import homekeeper.config
import homekeeper.test_case
import json


class TestHomekeeper(homekeeper.test_case.TestCase):
    def setup_method(self):
        super(TestHomekeeper, self).setup_method()
        self.patch('homekeeper')
        self.patch('homekeeper.common')
        self.patch('homekeeper.config')
        self.patch('homekeeper.main')
        self.setup_custom_homekeeper_json()
        self.setup_base_directory()
        self.setup_dotfiles_directory()
        self.os.chdir(self.os.getenv('HOME'))

    def setup_custom_homekeeper_json(self):
        self.homekeeper_json = self.home('custom', 'homekeeper.json')
        base_directory = self.home('custom_base')
        dotfiles_directory = self.home('custom_dotfiles')
        excludes = ['.git']
        data = {
            'base_directory': base_directory,
            'dotfiles_directory': dotfiles_directory,
            'excludes': excludes
        }
        self.touch(self.homekeeper_json)
        with self.fopen(self.homekeeper_json, 'w') as f:
            f.write(json.dumps(data))

    def setup_base_directory(self):
        self.base_directory = self.home('dotfiles', 'base')
        self.makedirs(self.base_directory)
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
            self.makedirs(self.path(self.base_directory, dirname))
        bash_local = self.path(self.base_directory, '.bash_local')
        with self.fopen(bash_local, 'w') as f:
            f.write('export BASE_DIRECTORY=1')

    def setup_dotfiles_directory(self):
        self.dotfiles_directory = self.home('dotfiles', 'main')
        self.makedirs(self.dotfiles_directory)
        bash_local = self.path(self.dotfiles_directory, '.bash_local')
        with self.fopen(bash_local, 'w') as f:
            f.write('export DOTFILES_DIRECTORY=1')
        self.touch(self.dotfiles_directory, '.bash_aliases')
        self.makedirs(self.path(self.dotfiles_directory, '.tmux'))

    def test_init_saves_config(self):
        self.os.chdir(self.dotfiles_directory)
        h = homekeeper.Homekeeper(pathname=self.homekeeper_json)
        h.init()
        with self.fopen(self.homekeeper_json, 'r') as f:
            data = json.loads(f.read())
        assert self.dotfiles_directory == data['dotfiles_directory']
