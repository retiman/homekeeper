import fake_filesystem
import fake_filesystem_shutil
import homekeeper.common
import logging
import mock
import pytest

logging.basicConfig(format='%(message)s', level=logging.DEBUG)


class TestCase(object):
    @pytest.fixture
    def os(self):
        return self.os

    def setup_method(self):
        self.fake_fs = fake_filesystem.FakeFilesystem()
        self.fake_fopen = fake_filesystem.FakeFileOpen(self.fake_fs)
        self.os = fake_filesystem.FakeOsModule(self.fake_fs)
        self.shutil = fake_filesystem_shutil.FakeShutilModule(self.fake_fs)
        self.patchers = []
        self.setup_os(self.os)

    def setup_os(self, os):
        os.environ['HOME'] = os.path.join(os.sep, 'home', 'johndoe')

    def teardown_method(self):
        for patcher in self.patchers:
            patcher.stop()
        del self.fake_fs

    def home(self):
        return self.os.getenv('HOME')

    def patch(self, module):
        self._patch(module, 'fopen', self.fake_fopen)
        self._patch(module, 'os', self.os)
        self._patch(module, 'shutil', self.shutil)

    def read_file(self, *args):
        filename = self.os.path.join(*args)
        with self.fake_fopen(filename, 'r') as f:
            return f.read()

    def setup_file(self, *args, **kwargs):
        return self._setup_file(self.os, args, kwargs)

    def setup_directory(self, *args):
        return self._setup_directory(self.os, args)

    def _setup_file(self, os, args, kwargs):
        filename = os.path.join(os.sep, *args)
        dirname = os.path.dirname(filename)
        self.setup_directory(dirname)
        contents = '' if ('data' not in kwargs) else kwargs['data']
        if os.path.exists(filename):
            os.unlink(filename)
        self.fake_fs.CreateFile(filename, contents=contents)
        return filename

    def _setup_directory(self, os, args):
        if args == []:
            return
        items = args
        if not args[0].startswith(os.sep):
            items = (os.sep,) + items
        dirname = os.path.join(*items)
        with mock.patch('homekeeper.common.os', os):
            homekeeper.common.makedirs(dirname)
        return dirname

    def _patch(self, module, name, fake):
        try:
            patcher = mock.patch(module + '.' + name, fake)
            patcher.start()
            self.patchers.append(patcher)
        except AttributeError:
            logging.error('can not patch: %s.%s', module, name)
