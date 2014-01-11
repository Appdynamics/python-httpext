from os.path import getmtime, join as path_join
from osext import filesystem as fs
from sh import which
import calendar
import httpext
import os
import tempfile
import unittest


class TestDownloadFunctions(unittest.TestCase):
    TEST_URI = 'http://www.example.com'

    _temp_files = []

    def setUp(self):
        pass

    def test_normal_use(self):
        local_file = tempfile.mkstemp(prefix='_test-httpext_')[1]
        self._temp_files.append(local_file)

        httpext.dl(self.TEST_URI, local_file)

        with open(local_file) as f:
            line = f.readline().strip()
            self.assertEqual(line, '<!doctype html>')
            self.assertIn('This domain is established to be used for illustrative examples in documents.', ' '.join(f.readlines()))

    def test_cached_response(self):
        local_file = tempfile.mkstemp(prefix='_test-httpext_')[1]
        self._temp_files.append(local_file)

        expected_file_path = path_join(os.environ['HOME'], '.cache', 'httpext', local_file)
        self._temp_files.append(expected_file_path)

        httpext.dl(self.TEST_URI, local_file)
        self.assertTrue(fs.isfile(expected_file_path))

        last_modified = httpext.get_last_modified_time(self.TEST_URI)
        file_time = getmtime(expected_file_path)
        self.assertEqual(file_time, calendar.timegm(last_modified))

    def test_append_url_contents(self):
        local_file = tempfile.mkstemp(prefix='_test-httpext_')[1]
        self._temp_files.append(local_file)

        with open(local_file, 'w') as f:
            f.write('Not HTML\n')

        httpext.append_url_contents(self.TEST_URI, local_file)

        with open(local_file) as f:
            first_line = f.readline().strip()
            self.assertEqual('Not HTML', first_line)
            self.assertEqual('<!doctype html>', f.readline().strip())

    def doCleanups(self):
        for file in self._temp_files:
            if fs.isfile(file):
                os.remove(file)
