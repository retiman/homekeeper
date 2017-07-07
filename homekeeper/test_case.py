import fake_filesystem
import fake_filesystem_shutil
import homekeeper.common
import logging
import mock

logging.basicConfig(format='%(message)s', level=logging.DEBUG)


class TestCase(object):
    def setup_method(self):
        self.fs = fake_filesystem.FakeFilesystem()
        self.fopen = fake_filesystem.FakeFileOpen(self.fs)
        self.os = fake_filesystem.FakeOsModule(self.fs)
        self.os.environ['HOME'] = self.os.path.join(self.os.sep, 'home',
                                                    'johndoe')
        self.shutil = fake_filesystem_shutil.FakeShutilModule(self.fs)
        self.patchers = []

    def teardown_method(self):
        for patcher in self.patchers:
            patcher.stop()
        del self.fs

    def home(self, *args):
        home_directory = self.os.getenv('HOME')
        return self.os.path.join(home_directory, *args)

    def patch(self, module):
        self._patch(module, 'fopen', self.fopen)
        self._patch(module, 'os', self.os)
        self._patch(module, 'shutil', self.shutil)

    def setup_file(self, *args, **kwargs):
        filename = self.os.path.join(self.os.sep, *args)
        dirname = self.os.path.dirname(filename)
        self.setup_directory(dirname)
        contents = '' if ('data' not in kwargs) else kwargs['data']
        self.fs.CreateFile(filename, contents=contents)
        return filename

    def setup_directory(self, *args):
        if args == []:
            return
        items = args
        if not args[0].startswith(self.os.sep):
            items = (self.os.sep,) + items
        dirname = self.os.path.join(*items)
        with mock.patch('homekeeper.common.os', self.os):
            homekeeper.common.makedirs(dirname)
        return dirname

    def _patch(self, module, name, fake):
        try:
            patcher = mock.patch(module + '.' + name, fake)
            patcher.start()
            self.patchers.append(patcher)
        except AttributeError:
            logging.error('can not patch: %s.%s', module, name)
