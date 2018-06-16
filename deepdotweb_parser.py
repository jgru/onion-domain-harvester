from datetime import date
from threading import Thread
import time
from bs4 import BeautifulSoup
import html_harvesting
from onion_domain import OnionDomain
from onion_domain_parser import AbstractDomainParser


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


def parse_domains():
    onion_domains = set()
    # create a list of threads
    threads = []
    results = [[] for t in targets]
    start_time = time.time()
    # In this case 'urls' is a list of urls to be crawled.
    for i in range(len(targets)):
        # We start one thread per url present.
        process = Thread(target=parse_market_page,
                         args=[targets[i], results, i])
        process.start()
        threads.append(process)

    # We now pause execution on the main thread by 'joining' all of our
    # started threads.
    # This ensures that each has finished processing the urls.
    for process in threads:
        process.join()

    print("Elapsed time: " + str(time.time() - start_time) + " secs")

    for li in results:
        for el in li:
            onion_domains.add(el)

    return onion_domains


@staticmethod
def parse_html(target_url):
    html = html_harvesting.load_cloudflare_page(target_url)
    # print(html)
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    return soup




def parse_market_page(target, results, idx):
    print("Parsing " + target + " in thread #" + str(idx))

    soup = parse_html(target)

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


def print_time(thread_name, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print(thread_name + "  " + time.ctime(time.time()))