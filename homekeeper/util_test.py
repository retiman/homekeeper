import homekeeper.testing
import homekeeper.util
import unittest

# pylint: disable=invalid-name
os = None
create_symlinks = homekeeper.util.create_symlinks
cleanup_symlinks = homekeeper.util.cleanup_symlinks
prepare_target = homekeeper.util.prepare_target
firstdir = homekeeper.util.firstdir
testing = homekeeper.testing

class UtilTest(unittest.TestCase):
    def setUp(self):
        self.filesystem, globals()['os'] = testing.init()
        self.home = os.getenv('HOME')

    def tearDown(self):
        del self.filesystem

    def test_create_symlinks(self):
        """Tests symlinking 'base/.vimrc' to '$HOME/.vimrc'."""
        source = os.path.join(testing.base_directory(), '.vimrc')
        target = os.path.join(self.home, '.vimrc')
        self.filesystem.CreateFile(source)
        self.assertTrue(os.path.exists(source))
        self.assertFalse(os.path.exists(target))
        create_symlinks(testing.base_directory(), self.home)
        self.assertTrue(os.path.exists(source))
        self.assertTrue(os.path.exists(target))
        self.assertTrue(os.path.islink(target))
        self.assertEquals(source, os.readlink(target))

    def test_create_symlinks_with_excludes(self):
        """Tests that 'base/.vimrc' can be excluded from symlinking."""
        source = os.path.join(testing.base_directory(), '.vimrc')
        target = os.path.join(self.home, '.vimrc')
        excludes = ['.vimrc']
        self.filesystem.CreateFile(source)
        self.assertTrue(os.path.exists(source))
        self.assertFalse(os.path.exists(target))
        create_symlinks(testing.base_directory(), self.home, excludes=excludes)
        self.assertTrue(os.path.exists(source))
        self.assertFalse(os.path.exists(target))
        self.assertFalse(os.path.islink(target))

    def test_create_symlinks_without_includes(self):
        """Tests that only 'base/.config' is symlinked.

        Without the 'includes' directive, the entire top level directory will be
        symlinked.
        """
        source = os.path.join(testing.base_directory(),
                              '.config',
                              'Terminal',
                              'terminalrc')
        target = os.path.join(self.home,
                              '.config',
                              'Terminal',
                              'terminalrc')
        self.filesystem.CreateFile(source)
        self.assertTrue(os.path.exists(source))
        self.assertFalse(os.path.exists(target))
        create_symlinks(testing.base_directory(),
                        self.home,
                        excludes=None,
                        includes=None)
        self.assertTrue(os.path.exists(source))
        self.assertTrue(os.path.exists(target))
        self.assertTrue(os.path.islink(os.path.join(self.home, '.config')))
        self.assertEquals(os.path.join(testing.base_directory(), '.config'),
                          os.readlink(os.path.join(self.home, '.config')))

    def test_create_symlinks_with_includes(self):
        """Tests that only 'terminalrc' is symlinked.

        With the 'includes' directive, only the most specific file or
        directory will be symlinked. That is, '.config/Terminal/terminalrc'
        will be symlinked, but everything else in the target '.config' directory
        will be left alone.

        This test ensures that unrelated files won't be clobbered by symlinking
        the 'terminalrc' file.
        """
        source = os.path.join(testing.base_directory(),
                              '.config',
                              'Terminal',
                              'terminalrc')
        target = os.path.join(self.home,
                              '.config',
                              'Terminal',
                              'terminalrc')
        unrelated = os.path.join(self.home,
                                 '.config',
                                 'user-dirs.dirs')
        includes = [os.path.join('.config', 'Terminal', 'terminalrc')]
        self.filesystem.CreateFile(source)
        self.filesystem.CreateFile(unrelated)
        self.assertTrue(os.path.exists(source))
        self.assertTrue(os.path.exists(unrelated))
        self.assertFalse(os.path.exists(target))
        create_symlinks(testing.base_directory(),
                        self.home,
                        excludes=None,
                        includes=includes)
        self.assertTrue(os.path.exists(source))
        self.assertTrue(os.path.exists(target))
        self.assertTrue(os.path.exists(unrelated),
                        msg='Unrelated file was clobbered.')
        self.assertFalse(os.path.islink(unrelated),
                         msg='Unrelated file was transformed into symlink.')
        self.assertTrue(os.path.isdir(os.path.dirname(target)),
                        msg='Target parent directory is no longer a directory.')
        self.assertFalse(os.path.islink(os.path.dirname(target)),
                         msg='Target parent should not be a symlink.')
        self.assertTrue(os.path.islink(target),
                        msg='Target is not a symlink as expected.')

    def test_cleanup_symlinks(self):
        """Tests that non-existant symlinks are removed."""
        self.filesystem.CreateFile('a.txt')
        os.symlink('a.txt', 'exists.txt')
        os.symlink('b.txt', 'nonexistent1.txt')
        os.symlink('c.txt', 'nonexistent2.txt')
        self.assertTrue(os.path.islink('nonexistent1.txt'))
        self.assertTrue(os.path.islink('nonexistent2.txt'))
        cleanup_symlinks('/')
        self.assertFalse(os.path.exists('nonexistent1.txt'))
        self.assertFalse(os.path.exists('nonexistent2.txt'))
        self.assertTrue(os.path.exists('exists.txt'))

    def test_prepare_target(self):
        """Tests that targets are removed before symlinking."""
        target = os.path.join(self.home, '.vimrc')
        self.filesystem.CreateFile(target)
        self.assertTrue(os.path.exists(target))
        prepare_target(target)
        self.assertFalse(os.path.exists(target))

    def test_prepare_target_creates_parent_directory(self):
        """Tests that target parent directories are created before symlinking.
        """
        target = os.path.join(self.home, '.foo', 'bar', 'bif')
        self.assertFalse(os.path.exists(target))
        prepare_target(target)
        self.assertFalse(os.path.exists(target))
        self.assertTrue(os.path.isdir(os.path.dirname(target)))

    def test_firstdir(self):
        """Tests that the first directory of a path is returned."""
        self.assertEquals('home', firstdir('home/johndoe/.vimrc'))
        self.assertEquals('home', firstdir('/home/johndoe/.vimrc'))
        self.assertEquals('.vimrc', firstdir('.vimrc'))
        self.assertEquals('', firstdir(''))
        self.assertEquals('', firstdir('/'))

