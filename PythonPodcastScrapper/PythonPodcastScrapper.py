import os
import sys
import requests
import fnmatch
import urllib.request

from bs4 import BeautifulSoup, SoupStrainer
from progressbar2 import progressbar # modules
from time import sleep

#Reference > https://ocefpaf.github.io/python4oceanographers/blog/2015/07/06/podcasts/

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
    else:
        output = open(fname, "wb")
    
    web_page = url_obj.open(url)

    if verbose:
        for key, value in web_page.headers.items():
            sys.stdout.writer("{} = {}\n".format(key, value))

    #if we already have teh whole file, there is no need to download it again.
    num_bytes = 0
    full_size = int(web_page.headers['Content-Length'])
    if full_size == current_size:
        msg = "File ({}) was already downloaded from URL ({})".format
        sys.stdout.write(msg(fname, url))
    elif full_size == 0:
        sys.stdout.write("Full file size equal zero!"
                         "Try again later or check the file.")
    else:
        if verbose:
            msg = "Downloading {:d} more bytes".format
            sys.stdout.write(msg(full_size - current_size))
        pbar = ProgressBar(maxval=full_size)
        pbar.start()
        while True:
            try:
                data = web_page.read(8192)
            except ValueError:
                break
            if not data:
                break
            output.write(data)
            num_bytes = num_bytes +len(data)
            pbar.update(num_bytes)
        pbar.finish()
    web_page.close()
    output.close()

    if verbose:
        msg = "Downloaded {} bytes from {}".format
        sys.stdout.write(msg(num_bytes, web_page.url))

pow= range(0, 101)
uri = ("https://dfkfj8j276wwv.cloudfront.net/episodes/c59ffe3e-4026-487f-a0d4-be8e3e2a3c37/3941082f84c9548e7c531014992a3c1095480aeb8aa5abb83966bbadf98f39d930d6d77c0fb5eac6c52bab3cdfd5c0bea992d9cf0f2fee7e4bb5590ee78c93c5/Harmontown%20Ep%20254.mp3")

for podcast in podcasts:
    url = uri(podcast)
    print(uurl + '\n')
    try:
        fname = url.split('/')[-1]
        download(fname, url, verbose=True)
    except HTTPError:
         print('Cannot download {}\n'.format(url))
    print('\n')
    sleep(2)