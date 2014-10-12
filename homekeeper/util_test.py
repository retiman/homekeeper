import fake_filesystem
import homekeeper.util
import unittest
import __builtin__

# pylint: disable=invalid-name
os = None
util = homekeeper.util

class UtilTest(unittest.TestCase):
    def setUp(self):
        self.filesystem = fake_filesystem.FakeFilesystem()
        globals()['os'] = fake_filesystem.FakeOsModule(self.filesystem)
        __builtin__.open = fake_filesystem.FakeFileOpen(self.filesystem)
        homekeeper.util.os = os

    def tearDown(self):
        del self.filesystem

    def test_cleanup_symlinks(self):
        self.filesystem.CreateFile('/a.txt')
        os.symlink('/a.txt', '/exists.txt')
        os.symlink('/b.txt', '/nonexistent1.txt')
        os.symlink('/c.txt', '/nonexistent2.txt')
        self.assertTrue(os.path.islink('/nonexistent1.txt'))
        self.assertTrue(os.path.islink('/nonexistent2.txt'))
        homekeeper.util.cleanup_symlinks('/')
        self.assertFalse(os.path.exists('/nonexistent1.txt'))
        self.assertFalse(os.path.exists('/nonexistent2.txt'))
        self.assertTrue(os.path.exists('/exists.txt'))

