import unittest

import homekeeper


class HomekeeperTest(unittest.TestCase):
    def setUp(self):
        self.homekeeper = homekeeper.Homekeeper()

    def tearDown(self):
        pass
