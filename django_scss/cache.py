from django_scss.settings import SCSS_MTIME_DELAY
from django.core.cache import cache
from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor
import os.path
import socket


def get_hexdigest(plaintext, length=None):
    digest = md5_constructor(smart_str(plaintext)).hexdigest()
    if length:
        return digest[:length]
    return digest


def get_cache_key(key):
    return ("django_scss.%s.%s" % (socket.gethostname(), key))


def get_mtime_cachekey(filename):
    return get_cache_key("mtime.%s" % get_hexdigest(filename))


def get_mtime(filename):
    if SCSS_MTIME_DELAY:
        key = get_mtime_cachekey(filename)
        mtime = cache.get(key)
        if mtime is None:
            mtime = os.path.getmtime(filename)
            cache.set(key, mtime, SCSS_MTIME_DELAY)
        return mtime
    return os.path.getmtime(filename)


def get_hashed_mtime(filename, length=12):
    try:
        filename = os.path.realpath(filename)
        mtime = str(int(get_mtime(filename)))
    except OSError:
        return None
    return get_hexdigest(mtime, length)
