from datetime import date
import time
import logging

from bs4 import BeautifulSoup, NavigableString

import html_harvesting
from onion_domain import OnionDomain


__author__ = 'gru'


targets = ["http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page",
           "http://uhwikih256ynt57t.onion/wiki/index.php/Darknet_Markets"]


def parse_html(target_url):
    html = html_harvesting.load_page(target_url)
    print(html)
    soup = BeautifulSoup(html, "html.parser")

    return soup


def parse_hidden_wiki_v1(target):
    onion_domains = set()
    start_time = time.time()
    logging.info("Parsing " + target)
    soup = parse_html(target)
    print(soup)
    entries = soup.find_all("a", class_="external text")
    for e in entries:
        url = e["href"]  # e.attrs["href"]

        if ".onion" not in url:
            continue

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


def clean_description(description):
    while description.startswith(" ") or description.startswith("-"):
                        description = description[1:]

    return  description


def parse_hidden_wiki_v2(target):
    onion_domains = set()
    start_time = time.time()
    logging.info("Parsing " + target)

    soup = parse_html(target)

    entries = soup.find_all("li")

    for e in entries:
        b = e.findChild("b")
        links = e.findAll("a")
        if links is not None:
            i = 0
            orig_title = ""
            for linkelem in links:

                url = linkelem.get('href')
                if url is not None:
                    if ".onion" not in url:
                        continue

                    title = linkelem.text
                    if i == 0:
                        orig_title = linkelem.text
                        title = orig_title
                    else:
                        title = orig_title + " - " + title
                    i += 1

                    if b is not None:
                        description = b.next_sibling
                    else:
                        description = linkelem.next_sibling

                    if description is None:
                        description = ""
                    description = clean_description(description)

                    parsed_domain = OnionDomain(url, title, description, date.today())
                    onion_domains.add(parsed_domain)

    logging.info("Elapsed time: " + str(time.time() - start_time) + " secs")

    return onion_domains


def parse_domains():
    onion_domains = set()
    for t in targets:
        onion_domains.update(parse_hidden_wiki_v2(t))
    
    return onion_domains











