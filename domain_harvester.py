__author__ = 'gru'


import urllib.request


from onion_domain import OnionDomain, OnionDbHandler
from deeptdotweb_parser import DeepdotwebParser


class HtmlHarvester:
    def __init__(self, target_page, data, hdr):
        self.target_page = target_page
        self.data = data
        if hdr is not None:
            self.hdr = hdr
        else:
            self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
                        # AppleWebKit/537.11 (KHTML, like Gecko)
                        # Chrome/23.0.1271.64
                        # Safari/537.11
                        'Accept': 'text/html,application/xhtml+xml,'
                                  'application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'}

    def load_page(self):
        req = urllib.request.Request(self.target_page, self.data, self.hdr)
        with urllib.request.urlopen(req) as response:
            html = response.read()
            return html








