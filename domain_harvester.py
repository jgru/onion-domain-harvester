__author__ = 'gru'


import urllib.request
import requests
import re
import cfscrape

class HtmlHarvester:

    proxies = {'http':  'socks5h://localhost:9050', 'https':
        'socks5h://localhost:9050'}

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

    def load_page(self, isSocks5H=True):
        if isSocks5H:
            return self.load_page_requests()
        else:
            return self.load_page_urllib()

    def load_page_urllib(self):
        req = urllib.request.Request(self.target_page, self.data, self.hdr)
        with urllib.request.urlopen(req) as response:
            html = response.read()
            return html

    def load_page_requests(self):
        session = requests.session()
        # use the socks5h protocol in order to enable remote DNS resolving in
        # case the local DNS resolving process fails
        session.proxies = self.proxies

        # Return the contents of the page
        return session.get(self.target_page).text

    def load_cloudflare_page(self):
        scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
        html = scraper.get(self.target_page).content
        return html

    CHK_IP_URL_A = "https://wtfismyip.com/text"
    CHK_IP_URL_B = "http://httpbin.org/ip"

    def check_tor_setup(self):
        session = requests.session()
        session.proxies = self.proxies



        orig_response = requests.get(self.CHK_IP_URL_B).text  # prints {
        # "origin": "5.102.254.76" }
        obfuscated_response = session.get(self.CHK_IP_URL_B).text  #
        # prints {
        # "origin": "67.205.146.164" }
        ip_pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        orig_ip = re.findall(ip_pattern, orig_response)[0]

        obfuscated_ip = re.findall(ip_pattern, obfuscated_response)[0]
        print("Orig IP: " + orig_ip + "\nObfuscated IP: " + obfuscated_ip
              +"\n")

        is_different = not orig_ip == obfuscated_ip

        orig_ip = requests.get(self.CHK_IP_URL_A).text.strip()
        obfuscated_ip = session.get(self.CHK_IP_URL_A).text.strip()  #
        print("Orig IP: " + orig_ip + "\nObfuscated IP: " + obfuscated_ip)

        return is_different and not(orig_ip == obfuscated_ip)








