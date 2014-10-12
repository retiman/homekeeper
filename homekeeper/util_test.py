import homekeeper.testing
import homekeeper.util
import unittest

# pylint: disable=invalid-name
os = None
create_symlinks = homekeeper.util.create_symlinks
cleanup_symlinks = homekeeper.util.cleanup_symlinks
testing = homekeeper.testing

class UtilTest(unittest.TestCase):
    def setUp(self):
        self.home = '/home/johndoe'
        self.filesystem, globals()['os'] = testing.create_fake_filesystem()

    def tearDown(self):
        del self.filesystem

    def test_create_symlinks(self):
        source = '/dotfiles/.vimrc'
        target = self.home + '/.vimrc'
        self.filesystem.CreateFile(source)
        self.assertTrue(os.path.exists(source))
        self.assertFalse(os.path.exists(target))
        create_symlinks('/dotfiles', self.home)
        self.assertTrue(os.path.exists(source))
        self.assertTrue(os.path.exists(target))
        self.assertTrue(os.path.islink(target))
        self.assertEquals(source, os.readlink(target))

    def test_create_symlinks_with_overrides(self):
        source = '/dotfiles/.vimrc'
        target = self.home + '/.vimrc'
        excludes = ['.vimrc']
        self.filesystem.CreateFile(source)
        self.assertTrue(os.path.exists(source))
        self.assertFalse(os.path.exists(target))
        create_symlinks('/dotfiles', self.home, excludes=excludes)
        self.assertTrue(os.path.exists(source))
        self.assertFalse(os.path.exists(target))
        self.assertFalse(os.path.islink(target))

    def test_cleanup_symlinks(self):
        self.filesystem.CreateFile('/a.txt')
        os.symlink('/a.txt', '/exists.txt')
        os.symlink('/b.txt', '/nonexistent1.txt')
        os.symlink('/c.txt', '/nonexistent2.txt')
        self.assertTrue(os.path.islink('/nonexistent1.txt'))
        self.assertTrue(os.path.islink('/nonexistent2.txt'))
        cleanup_symlinks('/')
        self.assertFalse(os.path.exists('/nonexistent1.txt'))
        self.assertFalse(os.path.exists('/nonexistent2.txt'))
        self.assertTrue(os.path.exists('/exists.txt'))

