__author__ = 'gru'

import socks
import socket
from bs4 import BeautifulSoup

from domain_harvester import HtmlHarvester
from onion_domain_parser import AbstractOnionDomainParser


class HiddenWikiParser(AbstractOnionDomainParser):

    target = "http://zqktlwi4fecvo6ri.onion"
    #target = "https://www.wikipedia.org"

    def __init__(self):
        self.onion_domains = set()

    def parse_market_list(self):
        HiddenWikiParser.parse_html(HiddenWikiParser.target)

    @staticmethod
    def parse_html(target_url):
        htmlHarvester = HtmlHarvester(target_url, None, None)
        html = htmlHarvester.load_page()
        print(html)
        soup = BeautifulSoup(html, "html.parser")
        # print(soup)
        return soup

    def print_harvested_domains(self):
        pass




import requests



if __name__ == "__main__":

    wiki_parser = HiddenWikiParser()
    wiki_parser.parse_market_list()






