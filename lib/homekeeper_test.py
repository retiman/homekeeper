import fake_filesystem
import unittest

import homekeeper


class HomekeeperTest(unittest.TestCase):
    def setUp(self):
        global os
        self.filesystem = fake_filesystem.FakeFilesystem()
        os = fake_filesystem.FakeOsModule(self.filesystem)
        config = {
            'dotfiles_directory': '.'
        }
        self.homekeeper = homekeeper.Homekeeper(config)

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
        pass
