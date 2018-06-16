__author__ = 'gru'

import socks
import socket
from deeptdotweb_parser import DeepdotwebParser
from domain_db import OnionDbHandler
from hiddenwiki_parser import HiddenWikiParser

DB_PATH = "./onion_domains.db"

def tor_setup():
    # MUST BE SET BEFORE IMPORTING URLLIB
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "localhost", 9050)
    # patch the socket module
    socket.socket = socks.socksocket

    # solution to prevent DNS leaks over a socks4/5 proxy
    def getaddrinfo(*args):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

    socket.getaddrinfo = getaddrinfo


def main():

    tor_setup()

    onion_domains = DeepdotwebParser().parse_domain_list()
    DeepdotwebParser.print_harvested_domains()

    onion_domains.union(HiddenWikiParser.parse_domain_list())
    HiddenWikiParser.print_harvested_domains()

    db_handler = OnionDbHandler(DB_PATH)
    db_handler.update_db(onion_domains)


if __name__ == "__main__":
    main()