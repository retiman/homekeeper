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
        self.patch('homekeeper.core')
        self.setup_base_directory()
        self.setup_dotfiles_directory()
        self.setup_overridden_paths()
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
        self.base_files = set([
            '.bash_aliases',
            '.bash_local',
            '.bash_profile',
            '.git',
            '.gitconfig',
            '.gitignore',
        ])
        self.base_directories = ([
            '.tmux',
            '.tmuxp',
            '.vim',
        ])
        for filename in self.base_files:
            self.touch(self.base_directory, filename)
        for dirname in self.base_directories:
            makedirs(self.path(self.base_directory, dirname))

    def setup_dotfiles_directory(self):
        self.dotfiles_directory = self.home('dotfiles', 'main')
        makedirs(self.dotfiles_directory)
        self.main_files = set(['.bash_aliases', '.bash_local'])
        self.main_directories = set(['.tmux', '.tmuxp'])
        for filename in self.main_files:
            self.touch(self.dotfiles_directory, filename)
        for dirname in self.main_directories:
            makedirs(self.path(self.dotfiles_directory, dirname))

    def setup_overridden_paths(self):
        for filename in self.main_files:
            path = self.path(self.base_directory, filename)
            with self.fopen(path, 'w') as f:
                f.write('base')
            path = self.path(self.dotfiles_directory, filename)
            with self.fopen(path, 'w') as f:
                f.write('main')
        for dirname in self.main_directories:
            self.touch(self.base_directory, dirname, 'base')
            self.touch(self.dotfiles_directory, dirname, 'main')

    def write_homekeeper_json(self, pathname, data):
        self.touch(pathname)
        with self.fopen(pathname, 'w') as f:
            f.write(json.dumps(data))

    def verify_original_files_still_exist(self):
        pass

    def verify_base_links(self, excludes):
        for item in self.base_files.union(self.base_directories):
            if item in self.main_files:
                continue
            if item in self.main_directories:
                continue
            if item in excludes:
                continue
            link = self.home(item)
            target = self.path(self.base_directory, item)
            assert os.path.islink(link)
            assert target == os.readlink(link)

    def verify_main_dotfiles_override_base_files(self):
        for filename in self.main_files:
            with self.fopen(self.home(filename), 'r') as f:
                assert 'main' == f.read()
        for dirname in self.main_directories:
            assert os.path.exists(self.home(dirname, 'main'))

    def test_init_saves_config(self):
        custom_dotfiles_directory = self.path(os.sep, 'custom')
        makedirs(custom_dotfiles_directory)
        os.chdir(custom_dotfiles_directory)
        homekeeper.Homekeeper(pathname=self.custom_homekeeper_json).init()
        with self.fopen(self.custom_homekeeper_json, 'r') as f:
            data = json.loads(f.read())
        assert custom_dotfiles_directory == data['dotfiles_directory']

    def test_init_with_default_config_path(self):
        h = homekeeper.Homekeeper()
        assert h.config.base_directory == self.base_directory
        assert h.config.dotfiles_directory == self.dotfiles_directory
        assert '.git' in h.config.excludes

    def test_keep(self):
        h = homekeeper.Homekeeper()
        h.keep()
        self.verify_original_files_still_exist()
        self.verify_base_links(h.config.excludes)
        self.verify_main_dotfiles_override_base_files()
