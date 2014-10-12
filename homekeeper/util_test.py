import fake_filesystem
import homekeeper.util
import unittest
import __builtin__

# pylint: disable=invalid-name
os = None
util = homekeeper.util

class UtilTest(unittest.TestCase):
    def setUp(self):
        self.filesystem = UtilTest.create_fake_filesystem()
        homekeeper.util.os = os

    def tearDown(self):
        del self.filesystem

    @staticmethod
    def create_fake_filesystem():
        filesystem = fake_filesystem.FakeFilesystem()
        globals()['os'] = fake_filesystem.FakeOsModule(filesystem)
        __builtin__.open = fake_filesystem.FakeFileOpen(filesystem)
        return filesystem

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

