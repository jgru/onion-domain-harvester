__author__ = 'gru'

import socks
import socket
import hiddenwiki_parser
import deepdotweb_parser

from domain_db import OnionDbHandler


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


def check_modules():
    if "parse_domains" in deepdotweb_parser.__dict__:
        print("API implemented")
    else:
        print("Warning: Not all API functions found in deepdotweb_parser")

    if "parse_domains" in hiddenwiki_parser.__dict__:
        print("API implemented")
    else:
        print("Warning: Not all API functions found in hiddenwiki_parser")


def print_harvested_domains(domains):
        for i in domains:
            print(i)
            print("˙\n------")
        print("Total amount: " + str(
            len(set(domains))) + " domains parsed")


def main():

    tor_setup()
    check_modules()

    onion_domains = deepdotweb_parser.parse_domains()
    onion_domains.update(hiddenwiki_parser.parse_domains())
    print_harvested_domains(onion_domains)

    db_handler = OnionDbHandler(DB_PATH)
    db_handler.update_db(onion_domains)


if __name__ == "__main__":
    main()