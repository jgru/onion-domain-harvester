from datetime import date
import time
import logging

from bs4 import BeautifulSoup

import html_harvesting
from onion_domain import OnionDomain


__author__ = 'gru'

targets = ["http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page",
           "http://uhwikih256ynt57t.onion/wiki/index.php/Darknet_Markets"]


def parse_html(target_url):
    html = html_harvesting.load_page(target_url)

    soup = BeautifulSoup(html, "html.parser")

    return soup


def parse_hidden_wiki(target):
    onion_domains = set()
    start_time = time.time()
    logging.info("Parsing " + target)
    soup = parse_html(target)
    entries = soup.find_all("a", class_="external text")
    for e in entries:
        url = e["href"]  # e.attrs["href"]
        title = e.text

        description = ""
        if e.next_sibling is not None:
            description = e.next_sibling.string
            while description.startswith(" ") or description.startswith("-"):
                description = description[1:]

        parsed_domain = OnionDomain(url, title, description, date.today())

        if parsed_domain is None:
            print(title, description)
        onion_domains.add(parsed_domain)

    logging.info("Elapsed time: " + str(time.time() - start_time) + " secs")
    return onion_domains


def parse_domains():
    onion_domains = set()
    for t in targets:
        onion_domains.update(parse_hidden_wiki(t))

    return onion_domains











