import os
import sys
import requests
import fnmatch
from bs4 import BeautifulSoup, SoupStrainer
from progressbar import progressbar


def urrllister(url):
    r = requests.get(url)
    soup = r.content
    urls = []
    for link in BeautifulSoup(soup, parse_only=SoupStrainer('a')):
        try:
            if link.has_attr('href'):
                urls.append(link['href'])
        except AttributeError:
            pass
        return urls

def filter_url(urls, filetype="*.mp3"):
    return (fname for fname in fnmatch.filter(urls, filetype))


try:
    from urllib.error import HTTPError
    from urllib.request import FancyURLopener
except ImportError:
    from urllib2 import HTTPError
    from urllib import FancyURLopener

class URLOpener(FancyURLopener):
    """Subclass to override error 206 (partial file being sent)."""
    def http_error_206(self, url, fp, errcode, errmsg, headers, data = None):
        pass # ignore the expected "non-error" code.

def download(fname, url, verbose=False):
    """Resume download."""
    current_size = 0
    url_obj = URLOpener()
    if os.path.exists(fname):
        output = open(fname, "ab")
        current_size = os.path.getsize(fname)
        #if the file exists, then download only the reminder.
        url_obj.addheader("Range", "bytes=%s-" % (current_size))
