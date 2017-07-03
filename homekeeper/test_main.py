import homekeeper.filesystem_testcase
import homekeeper.main


class TestMain(homekeeper.filesystem_testcase.FilesystemTestCase):
    def setup_method(self):
        super(TestMain, self).setup_method()
        self.patch_fs('homekeeper.main')
        self.main = homekeeper.main.Main()

    def test_symlink_removes_targets_first(self):
        source = self.touch(self.path(self.home(), 'dotfiles', '.vimrc'))
        target = self.touch(self.path(self.home(), '.vimrc'))
        self.main.symlink(source, target)
        assert self.os.path.islink(target)
