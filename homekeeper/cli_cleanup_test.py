import homekeeper.cli
import homekeeper.testing


cli = homekeeper.cli
lib = homekeeper.lib
BaseCliTest = homekeeper.testing.BaseCliTest


class CliCleanupTest(BaseCliTest):
    def test_cleanup_does_not_raise(self):
        self.run('cleanup')

    def test_cleanup_ignores_flags(self, os):
        dotfile = os.path.join(lib.get_home_directory(), '.dotfile')
        dotfile_link = os.path.join(lib.get_home_directory(), '.dotfile.link')
        lib.touch(dotfile)
        os.symlink(dotfile, dotfile_link)
        assert os.path.exists(dotfile)
        assert os.path.exists(dotfile_link)
        lib.remove(dotfile)
        result = self.run('--debug',
                          '--no-cleanup-symlinks',
                          '--no-overwrite',
                          '--config-path=/home/johndoe/.homekeeper.json',
                          'cleanup')
        assert result.exit_code == 0
        assert not os.path.exists(dotfile)
        assert not os.path.exists(dotfile_link)
