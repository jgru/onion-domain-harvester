
from threading import Thread
from datetime import date

import cfscrape
from bs4 import BeautifulSoup

from onion_domain_parser import AbstractOnionDomainParser
from onion_domain import OnionDomain


class DeepdotwebParser(AbstractOnionDomainParser):
    targets = ["https://www.deepdotweb.com/marketplace-directory"
                      "/categories/non-english/",
                      "https://www.deepdotweb.com/marketplace-directory"
                      "/categories/vendor-shops/",
                      "https://www.deepdotweb.com/marketplace-directory"
                      "/categories/markets/",
                      "https://www.deepdotweb.com/marketplace-directory"
                      "/categories/multisig-and-trusted/",
                      "https://www.deepdotweb.com/marketplace-directory"
                      "/categories/invite-markets/",
                      "https://www.deepdotweb.com/marketplace-directory"
                      "/categories/marketplaces/",
                      "https://www.deepdotweb.com/marketplace-directory"
                      "/categories/top-markets/"]

    def __init__(self):

        self.onion_domains = set()

    def parse_market_list(self):
        # create a list of threads
        threads = []
        results = [[] for t in self.targets]
        start_time = time.time()
        # In this case 'urls' is a list of urls to be crawled.
        for i in range(len(self.targets)):
            # We start one thread per url present.
            process = Thread(target=self.parse_market_page,
                             args=[self.targets[i], results, i])
            process.start()
            threads.append(process)

        # We now pause execution on the main thread by 'joining' all of our
        # started threads.
        # This ensures that each has finished processing the urls.
        for process in threads:
            process.join()

        print("Elapsed time: " + str(time.time() - start_time) + " secs")

        self.onion_domains = set()
        for li in results:
            for el in li:
                self.onion_domains.add(el)


    @staticmethod
    def parse_html(target_url):
        print(target_url)
        # htmlHarvester = HtmlHarvester(target_url, None, None)
        # html = htmlHarvester.load_page()
        scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
        # Or: scraper = cfscrape.CloudflareScraper()  # CloudflareScraper inherits from requests.Session
        html = scraper.get(target_url).content
        # print(html)
        soup = BeautifulSoup(html, "html.parser")
        # print(soup)
        return soup

    def print_harvested_domains(self):
        for i in self.onion_domains:
            print(i)
            print("˙\n------")
        print("Total amount: " + str(
            len(set(self.onion_domains))) + " domains parsed")

    @staticmethod
    def parse_market_page(target, results, idx):
        print("Parsing " + target + " in thread #" + str(idx))

        soup = DeepdotwebParser.parse_html(target)

        # title_divs = soup.find_all("div", {"class": "sabai-directory-title"})
        # link_divs = soup.find_all("div", {"class":
        # "sabai-directory-custom-fields"})
        entries = soup.find_all("div", {
            "class": "sabai-col-xs-9 sabai-directory-main"})
        for e in entries:
            url = ""
            description = ""
            title = e.find("div", {"class": "sabai-directory-title"}).text

            link_section = e.find("div", {"class": "sabai-field-value"})

            link = link_section.find('a', href=True)
            if link is not None:
                if "onion" in link["href"]:
                    url = (link["href"])

            elif link_section is not None and "onion" in link_section.string:
                url = link_section.string
            else:
                continue

            note_div = e.find("div", {"class": "sabai-directory-body"})
            p_elements = note_div.find_all("p")

            # Print "notes" section to corresponding onion-domain
            for element in p_elements:
                # Check, if there is no link, if so it is a notes-block
                if element.find('a') is None:
                    description = element.text

            parsed_domain = OnionDomain(url, title, description, date.today())
            results[idx].append(parsed_domain)


DB_PATH = "./onion_domains.db"

import time

# Define a function for the thread
def print_time(threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print(threadName + "  " + time.ctime(time.time()))