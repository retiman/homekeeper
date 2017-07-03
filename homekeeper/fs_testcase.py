import fake_filesystem
import fake_filesystem_shutil
import mock


class FilesystemTestCase(object):
    def setup_method(self):
        self.fs = fake_filesystem.FakeFilesystem()
        self.fopen = fake_filesystem.FakeFileOpen(self.fs)
        self.os = fake_filesystem.FakeOsModule(self.fs)
        self.shutil = fake_filesystem_shutil.FakeShutilModule(self.fs)
        self.patchers = []

    def teardown_method(self):
        for patcher in self.patchers:
            patchers.stop()
        del self.fs

    def patch_fs(self, module):
        self.patch(module, 'fopen', self.fopen)
        self.patch(module, 'os', self.os)
        self.patch(module, 'shutil', self.shutil)

    def patch(self, module, real, fake):
        if hasattr(module, real):
            patcher = mock.patch(module + '.' + real, fake)
            patcher.start()
            self.patchers.append(patcher)
