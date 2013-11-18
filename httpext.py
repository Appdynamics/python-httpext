# coding: utf-8

from os import utime as setfiletime
from os.path import join as path_join, isdir, basename, dirname
from shutil import copy2 as copy_file
from urllib2 import urlopen
import calendar
import datetime
import os
import time

import osext.filesystem as fs


def get_last_modified_time(url):
# TODO Handle timezones correctly
    req = urlopen(url)
    req.get_method = lambda: 'HEAD'
    last_modified = None

    for line in str(req.info()).split('\n'):
        if 'last-modified' in line.lower():
            last_modified = line.split(': ')[1].strip()
            last_modified = time.strptime(last_modified.replace(' GMT', ''), '%a, %d %b %Y %H:%M:%S')
            break

    if not last_modified:
        return None

    return last_modified


def dl(url, local_file, cache=True):
    last_modified = get_last_modified_time(url)
    filetime = None

    if last_modified:
        filetime = calendar.timegm(last_modified)

    cache_dir = path_join(os.environ['HOME'], '.cache', 'httpext')
    basename_fn = basename(local_file)
    cached_file = path_join(cache_dir, basename(basename_fn))

    if cache:
        if not isdir(cache_dir):
            os.makedirs(cache_dir)

        if fs.isfile(cached_file) and \
                fs.has_same_time(cached_file, filetime):
            copy_file(cached_file, path_join(dirname(local_file), basename_fn))

            return

    req = urlopen(url)

    with open(local_file, 'wb') as f:
        f.write(req.read())
        f.close()

        if filetime:
            setfiletime(local_file, (filetime, filetime))

        if cache:
            copy_file(local_file, cached_file)


def append_url_contents(url, local_file):
    with open(local_file, 'ab') as f:
        f.write(urlopen(url).read())
