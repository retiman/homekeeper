import fake_filesystem
import homekeeper
import unittest

# pylint: disable=invalid-name
os = None

class HomekeeperTest(unittest.TestCase):
    def setUp(self):
        # pylint: disable=global-statement
        global os
        self.filesystem = fake_filesystem.FakeFilesystem()
        os = fake_filesystem.FakeOsModule(self.filesystem)
        homekeeper.os = os
        homekeeper.util.os = os
        self.homekeeper = homekeeper.Homekeeper({'dotfiles_directory': '.'})

    def tearDown(self):
        del self.filesystem

    def test_configuration_defaults(self):
        self.homekeeper = homekeeper.Homekeeper()
        self.assertEquals(self.homekeeper.CONFIG_DEFAULTS['dotfiles_directory'],
                          self.homekeeper.config['dotfiles_directory'])
        self.assertRaises(ValueError, homekeeper.Homekeeper,
                          {'dotfiles_directory': os.getenv('HOME')})

    def test_branch(self):
        messages = ['# On branch foobar',
                    '# Your branch is ahead of \'origin/foobar\' by 2 commits.']
        homekeeper.sh = lambda command: '\n'.join(messages)
        self.assertEquals('foobar', self.homekeeper.branch())

    def test_commit_id(self):
        messages = ['commit a5f97835c71153123c10a664ff7d539dac02aada',
                    'Author: Min Huang <min.huang@alumni.usc.edu>',
                    'Date:   Tue Nov 19 18:04:34 2013 -0800']
        homekeeper.sh = lambda command: '\n'.join(messages)
        self.assertEquals('a5f97835c71153123c10a664ff7d539dac02aada',
                          self.homekeeper.commit_id())

    def test_remove_broken_symlinks(self):
        self.filesystem.CreateFile('/a.txt')
        os.symlink('/a.txt', '/exists.txt')
        os.symlink('/b.txt', '/nonexistent1.txt')
        os.symlink('/c.txt', '/nonexistent2.txt')
        self.assertTrue(os.path.islink('/nonexistent1.txt'))
        self.assertTrue(os.path.islink('/nonexistent2.txt'))
        homekeeper._remove_broken_symlinks('/')
        self.assertFalse(os.path.exists('/nonexistent1.txt'))
        self.assertFalse(os.path.exists('/nonexistent2.txt'))
        self.assertTrue(os.path.exists('/exists.txt'))

    def test_link_dotfiles(self):
        homekeeper.os.getenv = lambda var: '/home/johndoe'
        dotfiles_directory = '/home/johndoe/personal/dotfiles'
        config = {'dotfiles_directory': dotfiles_directory}
        self.filesystem.CreateFile(dotfiles_directory + '/.vimrc')
        self.homekeeper = homekeeper.Homekeeper(config)
        self.homekeeper.link()
        self.assertTrue(os.path.exists('/home/johndoe/personal/dotfiles/'
                                       '.vimrc'))
        self.assertTrue(os.path.islink('/home/johndoe/.vimrc'))
        self.assertTrue(os.path.exists('/home/johndoe/.vimrc'))
        self.assertEquals('/home/johndoe/personal/dotfiles/.vimrc',
                          os.readlink('/home/johndoe/.vimrc'))
