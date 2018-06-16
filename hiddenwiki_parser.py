from datetime import date
import time
from bs4 import BeautifulSoup
import html_harvesting
from onion_domain import OnionDomain

__author__ = 'gru'

target = "http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page"


def parse_html(target_url):
    html = html_harvesting.load_page(target_url)
    #print(html)
    soup = BeautifulSoup(html, "html.parser")
    #print(soup)
    return soup


def parse_domains():
    onion_domains = set()
    start_time = time.time()
    print("Parsing " + target)
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

    print("Elapsed time: " + str(time.time() - start_time) + " secs")

    return onion_domains






