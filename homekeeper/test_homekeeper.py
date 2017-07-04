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

    def setup_files(self):
        self.makedirs(self.home())
