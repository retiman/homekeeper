import fake_filesystem
import fake_filesystem_shutil
import mock


class FilesystemTestCase(object):
    def setup_method(self):
        self.fs = fake_filesystem.FakeFilesystem()
        self.fopen = fake_filesystem.FakeFileOpen(self.fs)
        self.os = fake_filesystem.FakeOsModule(self.fs)
        self.os.environ['HOME'] = self.path('', 'home', 'johndoe')
        self.shutil = fake_filesystem_shutil.FakeShutilModule(self.fs)
        self.patchers = []

    def teardown_method(self):
        for patcher in self.patchers:
            patcher.stop()
        del self.fs

    def home(self):
        return self.os.getenv('HOME')

    def path(self, *args):
        return self.os.path.join(*args)

    def touch(self, path):
        self.fs.CreateFile(path)
        return path

    def patch_fs(self, module):
        self.patch(module, 'fopen', self.fopen)
        self.patch(module, 'os', self.os)
        self.patch(module, 'shutil', self.shutil)

    def patch(self, module, name, fake):
        try:
            patcher = mock.patch(module + '.' + name, fake)
            patcher.start()
            self.patchers.append(patcher)
        except AttributeError:
            print 'Can not patch: %s.%s' % (module, name)
