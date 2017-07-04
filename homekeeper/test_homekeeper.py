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
        self.setup_base_directory()
        self.setup_dotfiles_directory()

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

    def test_foo(self):
        pass
