__author__ = 'gru'

import socks
import socket
from datetime import date
from bs4 import BeautifulSoup

from domain_harvester import HtmlHarvester
from onion_domain_parser import AbstractDomainParser
from onion_domain import OnionDomain



class HiddenWikiParser(AbstractDomainParser):

    targets = "http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page"
    #target = "https://www.wikipedia.org"
    onion_domains = set()


    @classmethod
    def parse_domain_list(cls):
        return cls.parse_domains()

    @staticmethod
    def parse_html(target_url):
        htmlHarvester = HtmlHarvester(target_url, None, None)
        html = htmlHarvester.load_page()
        #print(html)
        soup = BeautifulSoup(html, "html.parser")
        #print(soup)
        return soup

    @classmethod
    def parse_domains(cls):
        soup = cls.parse_html(cls.targets)
        entries = soup.find_all("a", class_="external text")
        for e in entries:
            url = e["href"]  # e.attrs["href"]
            title = e.text

            description = ""
            if e.next_sibling is not None:
                description = e.next_sibling.string
                while description.startswith(" ") or description.startswith(
                        "-"):
                    description = description[1:]

            parsed_domain = OnionDomain(url, title, description, date.today())
            if parsed_domain is None:
                print(title, description)
            cls.onion_domains.add(parsed_domain)

        return cls.onion_domains

if __name__ == "__main__":

    wiki_parser = HiddenWikiParser()
    wiki_parser.parse_domain_list()
    wiki_parser.print_harvested_domains()





