import homekeeper.testing
import homekeeper.util
import unittest

# pylint: disable=invalid-name
os = None
create_symlinks = homekeeper.util.create_symlinks
cleanup_symlinks = homekeeper.util.cleanup_symlinks
cleanup_target = homekeeper.util.cleanup_target
testing = homekeeper.testing

class UtilTest(unittest.TestCase):
    def setUp(self):
        self.filesystem, globals()['os'] = testing.init()
        self.home = os.getenv('HOME')

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

    def test_create_symlinks_with_includes(self):
        source = '/dotfiles/.config/Terminal/terminalrc'
        target = self.home + '/.config/Terminal/terminalrc'
        includes = ['.config/Terminal/terminalrc']
        self.filesystem.CreateFile(source)
        self.assertTrue(os.path.exists(source))
        self.assertFalse(os.path.exists(target))
        create_symlinks(
            '/dotfiles', self.home,
            excludes=None, includes=includes)
        self.assertTrue(os.path.exists(source)) # source exists?
        self.assertTrue(os.path.exists(target)) # target exists?
        # target parent dir is still a dir
        self.assertTrue(os.path.isdir(os.path.dirname(target)))
        self.assertTrue(os.path.islink(target)) # target is link?

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

    def test_cleanup_target(self):
        target = self.home + '/.vimrc'
        self.filesystem.CreateFile(target)
        self.assertTrue(os.path.exists(target))
        cleanup_target(target)
        self.assertFalse(os.path.exists(target))

