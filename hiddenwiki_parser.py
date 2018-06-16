__author__ = 'gru'

import socks
import socket
from bs4 import BeautifulSoup

from domain_harvester import HtmlHarvester
from onion_domain_parser import AbstractOnionDomainParser
import main_harvester


class HiddenWikiParser(AbstractOnionDomainParser):

    target = "http://zqktlwi4fecvo6ri.onion"
    target = "http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page"
    #target = "https://www.wikipedia.org"

    def __init__(self):
        self.onion_domains = set()

    def parse_domain_list(self):
        self.parse_domains()

    @staticmethod
    def parse_html(target_url):
        main_harvester.tor_setup()
        htmlHarvester = HtmlHarvester(target_url, None, None)
        html = htmlHarvester.load_page()
        #print(html)
        soup = BeautifulSoup(html, "html.parser")
        #print(soup)
        return soup

    def parse_domains(self):
        soup = self.parse_html(self.target)
        entries = soup.find_all("a", class_="external text")
        for e in entries:
            print(e)

    def print_harvested_domains(self):
        pass


if __name__ == "__main__":

    wiki_parser = HiddenWikiParser()
    wiki_parser.parse_domain_list()






