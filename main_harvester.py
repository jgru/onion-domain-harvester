__author__ = 'gru'

import socks
import socket
from deeptdotweb_parser import DeepdotwebParser
from onion_domain import OnionDbHandler
from domain_harvester import HtmlHarvester

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

    deep_parser = DeepdotwebParser()
    deep_parser.parse_domain_list()
    deep_parser.print_harvested_domains()

    db_handler = OnionDbHandler(DB_PATH)
    db_handler.update_db(deep_parser.onion_domains)


if __name__ == "__main__":
    main()