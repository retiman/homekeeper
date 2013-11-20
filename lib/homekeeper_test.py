import mox
import unittest

import homekeeper


class HomekeeperTest(unittest.TestCase):
    def setUp(self):
        config = {
            'dotfiles_directory': '.'
        }
        self.homekeeper = homekeeper.Homekeeper(config)

    def tearDown(self):
        pass
