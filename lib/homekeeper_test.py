import fake_filesystem
import unittest

import homekeeper


class HomekeeperTest(unittest.TestCase):
    def setUp(self):
        global os
        self.filesystem = fake_filesystem.FakeFilesystem()
        os = fake_filesystem.FakeOsModule(self.filesystem)
        homekeeper.os = os
        self.homekeeper = homekeeper.Homekeeper({'dotfiles_directory': '.'})

    def tearDown(self):
        del self.filesystem

    def test_branch(self):
        messages = ['# On branch foobar',
                    '# Your branch is ahead of \'origin/foobar\' by 2 commits.']
        homekeeper._sh = lambda command: '\n'.join(messages)
        self.assertEquals('foobar', self.homekeeper.branch())

    def test_commit_id(self):
        messages = ['commit a5f97835c71153123c10a664ff7d539dac02aada',
                    'Author: Min Huang <min.huang@alumni.usc.edu>',
                    'Date:   Tue Nov 19 18:04:34 2013 -0800']
        homekeeper._sh = lambda command: '\n'.join(messages)
        self.assertEquals('a5f97835c71153123c10a664ff7d539dac02aada',
                          self.homekeeper.commit_id())

    def test_remove_broken_symlinks(self):
        self.filesystem.CreateFile('/a.txt')
        os.symlink('/a.txt', '/exists.txt')
        os.symlink('/b.txt', '/nonexistent1.txt')
        os.symlink('/c.txt', '/nonexistent2.txt')
        self.assertTrue(os.path.islink('/nonexistent1.txt'))
        self.assertTrue(os.path.islink('/nonexistent2.txt'))
        self.homekeeper._Homekeeper__remove_broken_symlinks('/')
        self.assertFalse(os.path.exists('/nonexistent1.txt'))
        self.assertFalse(os.path.exists('/nonexistent2.txt'))
        self.assertTrue(os.path.exists('/exists.txt'))

    def test_link_dotfiles(self):
        homekeeper.os.getenv = lambda var: '/home/johndoe'
        dotfiles_directory = '/home/johndoe/personal/dotfiles'
        config = {'dotfiles_directory': dotfiles_directory}
        self.filesystem.CreateFile(dotfiles_directory + '/vimrc')
        self.homekeeper = homekeeper.Homekeeper(config)
        self.homekeeper.link()
        self.assertTrue(os.path.exists('/home/johndoe/personal/dotfiles/vimrc'))
        self.assertTrue(os.path.islink('/home/johndoe/.vimrc'))
        self.assertTrue(os.path.exists('/home/johndoe/.vimrc'))
        self.assertEquals('/home/johndoe/personal/dotfiles/vimrc',
                          os.readlink('/home/johndoe/.vimrc'))

    def test_link_scripts(self):
        homekeeper.os.getenv = lambda var: '/home/johndoe'
        dotfiles_directory = '/home/johndoe/personal/dotfiles'
        scripts_directory = '/home/johndoe/personal/scripts'
        config = {
            'dotfiles_directory': dotfiles_directory,
            'scripts_directory': scripts_directory
        }
        self.filesystem.CreateFile(scripts_directory + '/myscript')
        self.homekeeper = homekeeper.Homekeeper(config)
        self.homekeeper.link()
        self.assertTrue(os.path.islink('/home/johndoe/bin/myscript'))
        self.assertTrue(os.path.exists('/home/johndoe/bin/myscript'))
        self.assertEquals('/home/johndoe/personal/scripts/myscript',
                          os.readlink('/home/johndoe/bin/myscript'))
