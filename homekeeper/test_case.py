import fake_filesystem
import fake_filesystem_shutil
import logging
import mock

from homekeeper.common import makedirs

logging.basicConfig(format='%(message)s', level=logging.DEBUG)


class TestCase(object):
    def setup_method(self):
        self.fs = fake_filesystem.FakeFilesystem()
        self.fopen = fake_filesystem.FakeFileOpen(self.fs)
        self.os = fake_filesystem.FakeOsModule(self.fs)
        self.os.environ['HOME'] = self.path(self.os.sep, 'home', 'johndoe')
        self.shutil = fake_filesystem_shutil.FakeShutilModule(self.fs)
        self.patchers = []

    def teardown_method(self):
        for patcher in self.patchers:
            patcher.stop()
        del self.fs

    def home(self, *args):
        home_directory = self.os.getenv('HOME')
        return self.os.path.join(home_directory, *args)

    def path(self, *args):
        return self.os.path.join(*args)

    def touch(self, *args):
        with mock.patch('homekeeper.common.os', self.os):
            pathname = self.path(*args)
            dirname = self.os.path.dirname(pathname)
            makedirs(dirname)
            self.fs.CreateFile(pathname)
            return pathname

    def patch(self, module):
        self._patch(module, 'fopen', self.fopen)
        self._patch(module, 'os', self.os)
        self._patch(module, 'shutil', self.shutil)

    def _patch(self, module, name, fake):
        try:
            patcher = mock.patch(module + '.' + name, fake)
            patcher.start()
            self.patchers.append(patcher)
        except AttributeError:
            logging.error('can not patch: %s.%s', module, name)
