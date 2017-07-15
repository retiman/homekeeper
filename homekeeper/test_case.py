import contextlib
import pyfakefs.fake_filesystem
import pyfakefs.fake_filesystem_shutil
import homekeeper.common
import json
import logging
import mock
import pytest

fake_filesystem = pyfakefs.fake_filesystem
fake_filesystem_shutil = pyfakefs.fake_filesystem_shutil
logging.basicConfig(format='%(message)s', level=logging.DEBUG)


# pylint: disable=attribute-defined-outside-init
# pylint: disable=no-self-use
# pylint: disable=too-many-instance-attributes
class TestCase(object):
    def setup_method(self):
        self.fake_fs = fake_filesystem.FakeFilesystem()
        self.fake_fopen = fake_filesystem.FakeFileOpen(self.fake_fs)
        self.fake_os = fake_filesystem.FakeOsModule(self.fake_fs)
        self.fake_shutil = fake_filesystem_shutil.FakeShutilModule(self.fake_fs)
        self.patchers = []
        self.setup_os(self.fake_os)
        self.setup_configuration(self.fake_os)

    def setup_os(self, os):
        os.environ['HOME'] = os.path.join(os.sep, 'home', 'johndoe')
        self.home = os.getenv('HOME')
        self.setup_directory(self.home)

    def setup_configuration(self, os):
        with contextlib.nested(mock.patch('homekeeper.common.os', self.fake_os),
                               homekeeper.common.cd(self.home)):
            self.base_directory = os.path.abspath('base')
            self.dotfiles_directory = os.path.abspath('dotfiles')
            self.custom_directory = os.path.abspath('custom')
            self.setup_directory(self.base_directory)
            self.setup_directory(self.dotfiles_directory)
            self.setup_directory(self.custom_directory)
            self.setup_directory(self.custom_directory, 'base')
            self.setup_directory(self.custom_directory, 'dotfiles')
        data = json.dumps({
            'base_directory': self.base_directory,
            'dotfiles_directory': self.dotfiles_directory,
            'excludes': ['.git', '.gitignore'],
            'includes': [os.path.join(self.home, '.foo', 'foorc')],
        })
        self.setup_file(self.home, '.homekeeper.json', data=data)
        data = json.dumps({
            'base': os.path.join(self.custom_directory, 'base'),
            'directory': os.path.join(self.custom_directory, 'dotfiles'),
            'excludes': ['.git'],
            'cherrypicks': [os.path.join(self.home, '.bar', 'barrc')],
        })
        self.setup_file(self.home, 'custom', '.homekeeper.json', data=data)

    def teardown_method(self):
        for patcher in self.patchers:
            patcher.stop()
        del self.fake_fs

    @pytest.fixture
    def os(self):
        return self.fake_os

    def patch(self, module):
        self._patch(module, 'fopen', self.fake_fopen)
        self._patch(module, 'os', self.fake_os)
        self._patch(module, 'shutil', self.fake_shutil)

    def read_file(self, *args):
        return self._read_file(self.fake_os, self.fake_fopen, *args)

    def setup_file(self, *args, **kwargs):
        return self._setup_file(self.fake_os, args, kwargs)

    def setup_directory(self, *args):
        return self._setup_directory(self.fake_os, args)

    def _read_file(self, os, fopen, *args):
        filename = os.path.join(*args)
        with fopen(filename, 'r') as f:
            return f.read()

    def _setup_file(self, os, args, kwargs):
        filename = os.path.join(*args) # pylint: disable=star-args
        dirname = os.path.dirname(filename)
        self.setup_directory(dirname)
        contents = '' if ('data' not in kwargs) else kwargs['data']
        if os.path.exists(filename):
            os.unlink(filename)
        self.fake_fs.CreateFile(filename, contents=contents)
        return filename

    def _setup_directory(self, os, args):
        dirname = os.path.join(*args) # pylint: disable=star-args
        if dirname == '' or dirname == os.sep:
            return
        with mock.patch('homekeeper.common.os', os):
            homekeeper.common.makedirs(dirname)
        return dirname

    def _patch(self, module, name, fake):
        try:
            patcher = mock.patch(module + '.' + name, fake)
            patcher.start()
            self.patchers.append(patcher)
        except AttributeError:
            logging.debug('can not patch: %s.%s', module, name)
