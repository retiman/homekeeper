import homekeeper.testing
import homekeeper.util
import unittest

os = None
cleanup_symlinks = homekeeper.util.cleanup_symlinks
create_symlinks = homekeeper.util.create_symlinks
firstdir = homekeeper.util.firstdir
prepare_target = homekeeper.util.prepare_target
restore = homekeeper.util.restore
shutil = None
testing = homekeeper.testing

class UtilTest(unittest.TestCase):
    def setUp(self):
        global os, shutil
        self.filesystem, os, shutil = testing.init()
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

    def test_create_symlinks_with_commonprefix_cherrypicks(self):
        """Tests that '.a/b' can be included without interfering with '.ab'."""
        source = os.path.join(testing.base_directory(), '.a', 'b')
        target = os.path.join(self.home, '.a', 'b')
        unrelated = os.path.join(testing.base_directory(), '.ab')
        cherrypicks = [os.path.join('.a', 'b')]
        self.filesystem.CreateFile(source)
        self.filesystem.CreateFile(unrelated)
        self.assertTrue(os.path.exists(source))
        self.assertFalse(os.path.exists(target))
        create_symlinks(testing.base_directory(),
                        self.home,
                        excludes=None,
                        cherrypicks=cherrypicks)
        self.assertTrue(os.path.exists(source))
        self.assertTrue(os.path.exists(target))
        self.assertTrue(os.path.exists(unrelated),
                        msg='Unrelated file was clobbered.')
        self.assertTrue(os.path.islink(os.path.join(self.home, '.ab')),
                        msg='Unrelated file was not symlinked.')
        self.assertTrue(os.path.isdir(os.path.dirname(target)),
                        msg='Target parent directory is no longer a directory.')
        self.assertFalse(os.path.islink(os.path.dirname(target)),
                         msg='Target parent should not be a symlink.')
        self.assertTrue(os.path.islink(target),
                        msg='Target is not a symlink as expected.')

    def test_create_symlinks_without_cherrypicks(self):
        """Tests that only 'base/.config' is symlinked.

        Without the 'cherrypicks' directive, the entire top level directory will
        be symlinked.
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
                        cherrypicks=None)
        self.assertTrue(os.path.exists(source))
        self.assertTrue(os.path.exists(target))
        self.assertTrue(os.path.islink(os.path.join(self.home, '.config')))
        self.assertEquals(os.path.join(testing.base_directory(), '.config'),
                          os.readlink(os.path.join(self.home, '.config')))

    def test_create_symlinks_with_cherrypicks(self):
        """Tests that only 'terminalrc' is symlinked.

        With the 'cherrypicks' directive, only the most specific file or
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
        cherrypicks = [os.path.join('.config', 'Terminal', 'terminalrc')]
        self.filesystem.CreateFile(source)
        self.filesystem.CreateFile(unrelated)
        self.assertTrue(os.path.exists(source))
        self.assertTrue(os.path.exists(unrelated))
        self.assertFalse(os.path.exists(target))
        create_symlinks(testing.base_directory(),
                        self.home,
                        excludes=None,
                        cherrypicks=cherrypicks)
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

    def test_restore_file(self):
        """Tests symlinking 'base/.vimrc' to '$HOME/.vimrc' and then restoring
        will undo the action.
        """
        source = os.path.join(testing.base_directory(), '.vimrc')
        target = os.path.join(self.home, '.vimrc')
        self.filesystem.CreateFile(source)
        self.assertTrue(os.path.exists(source))
        self.assertFalse(os.path.exists(target))
        create_symlinks(testing.base_directory(), self.home)
        restore(testing.base_directory(), self.home)
        self.assertTrue(os.path.exists(source))
        self.assertTrue(os.path.exists(target))
        self.assertFalse(os.path.islink(source))
        self.assertFalse(os.path.islink(target))

    def test_restore_directory(self):
        """Tests symlinking directory 'base/.foo' to '$HOME/.foo' and then
        restoring will undo the action.
        """
        source = os.path.join(testing.base_directory(), '.foo', 'bar')
        target = os.path.join(self.home, '.foo', 'bar')
        os.makedirs(source)
        shutil.rmtree(target)
        self.assertTrue(os.path.exists(source))
        self.assertFalse(os.path.exists(target))
        create_symlinks(testing.base_directory(), self.home)
        restore(testing.base_directory(), self.home)
        self.assertTrue(os.path.exists(os.path.join(self.home, '.foo')))
        self.assertFalse(os.path.islink(os.path.join(self.home, '.foo')))
        self.assertTrue(os.path.exists(os.path.join(self.home, '.foo', 'bar')))
        self.assertFalse(os.path.islink(os.path.join(self.home, '.foo', 'bar')))

    def test_restore_with_excludes(self):
        """Test that excluded files are not restored."""
        source = os.path.join(testing.base_directory(), '.vimrc')
        unrelated = os.path.join(testing.base_directory(), '.git')
        excludes = ['.git']
        self.filesystem.CreateFile(source)
        self.filesystem.CreateFile(unrelated)
        self.assertTrue(os.path.exists(unrelated))
        self.assertFalse(os.path.exists(os.path.join(self.home, '.git')))
        create_symlinks(testing.base_directory(), self.home, excludes=excludes)
        restore(testing.base_directory(), self.home, excludes=excludes)
        self.assertFalse(os.path.exists(os.path.join(self.home, '.git')))

    def test_restore_with_cherrypicks(self):
        """Test that restoring cherrypicked files does not clobber other files.
        """
        source = os.path.join(testing.base_directory(), '.a', 'b', 'c')
        unrelated = os.path.join(self.home, '.a', 'd')
        cherrypicks = [os.path.join('.a', 'b', 'c')]
        self.filesystem.CreateFile(source)
        self.filesystem.CreateFile(unrelated)
        self.assertTrue(os.path.exists(unrelated))
        create_symlinks(testing.base_directory(),
                        self.home,
                        cherrypicks=cherrypicks)
        restore(testing.base_directory(),
                self.home,
                cherrypicks=cherrypicks)
        self.assertTrue(os.path.exists(unrelated))
        self.assertFalse(os.path.islink(unrelated))
        self.assertTrue(os.path.exists(os.path.join(self.home, '.a', 'b', 'c')))
        self.assertFalse(os.path.islink(os.path.join(self.home,
                                                     '.a',
                                                     'b',
                                                     'c')))

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

