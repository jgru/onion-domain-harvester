__author__ = 'gru'

import urllib.request
import cfscrape

data = None
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
                        # AppleWebKit/537.11 (KHTML, like Gecko)
                        # Chrome/23.0.1271.64
                        # Safari/537.11
                        'Accept': 'text/html,application/xhtml+xml,'
                                  'application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'}


def load_page(target_page):
    req = urllib.request.Request(target_page, data, hdr)
    with urllib.request.urlopen(req) as response:
        html = response.read()
        return html


def load_cloudflare_page(target_page):
    scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
    html = scraper.get(target_page).content
    return html


