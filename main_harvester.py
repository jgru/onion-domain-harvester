__author__ = 'gru'

import subprocess
import argparse
import socks
import socket
import hiddenwiki_parser
import deepdotweb_parser

from domain_db import OnionDbHandler


def tor_setup():
    # MUST BE SET BEFORE IMPORTING URLLIB
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "localhost", 9050)
    # patch the socket module
    socket.socket = socks.socksocket
    socket.timeout = 5
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


def main(db):

    tor_process = start_tor_service()
    tor_setup()
    check_modules()

    onion_domains = deepdotweb_parser.parse_domains()
    onion_domains.update(hiddenwiki_parser.parse_domains())
    print_harvested_domains(onion_domains)
    stop_tor(tor_process)

    db_handler = OnionDbHandler(db)
    db_handler.update_db(onion_domains)


SPECIFIC_STRING = "Bootstrapped 100%"


def start_tor_service():
    p = subprocess.Popen(["tor"], stdout=subprocess.PIPE, universal_newlines=True)
    print("Tor started")

    # Wait until tor setup is complete
    while True:
        output = p.stdout.readline()
        print(output.strip())
        if SPECIFIC_STRING in output:
            print("Tor setup complete")
            break

    return p


def stop_tor(p):
    p.terminate()


if __name__ == "__main__":
    print("Starting onion_domain harvester")
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--database", required=False, default="./onion_domains.db",
                        help="path to database (will be created if not existing")
    args = parser.parse_args()

    main(args.database)
