import logging
import sys
import subprocess
import argparse
import socket
import socks
import hiddenwiki_parser
import deepdotweb_parser

from domain_db import OnionDbHandler


__author__ = 'gru'


def tor_setup():
    # MUST BE SET BEFORE IMPORTING URLLIB
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "localhost", 9050)
    logging.info("Set default proxy")
    # patch the socket module
    socket.socket = socks.socksocket
    logging.info("Set socks")
    socket.timeout = 10
    # solution to prevent DNS leaks over a socks4/5 proxy
    def getaddrinfo(*args):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

    socket.getaddrinfo = getaddrinfo


def check_modules():
    if "parse_domains" in deepdotweb_parser.__dict__:
        logging.info("API implemented")
    else:
        logging.info("Warning: Not all API functions found in deepdotweb_parser")

    if "parse_domains" in hiddenwiki_parser.__dict__:
        logging.info("API implemented")
    else:
        logging.info("Warning: Not all API functions found in hiddenwiki_parser")


def print_harvested_domains(domains):
    for i in domains:
        logging.info(i)
        logging.info("\n------")
    logging.info("Total amount: " + str(
        len(set(domains))) + " domains parsed")


def main(db_dir):

    tor_process = start_tor_service()
    tor_setup()
    check_modules()

    onion_domains = deepdotweb_parser.parse_domains()
    onion_domains.update(hiddenwiki_parser.parse_domains())
    print_harvested_domains(onion_domains)
    stop_tor(tor_process)

    db_handler = OnionDbHandler(db_dir)
    db_handler.update_db(onion_domains)


SPECIFIC_STRING = "Bootstrapped 100%"


def start_tor_service():
    logging.info("Trying to start Tor")
    p = subprocess.Popen(["tor"], stdout=subprocess.PIPE, universal_newlines=True)
    logging.info("Tor started")

    # Wait until tor setup is complete
    while True:
        output = p.stdout.readline()
        logging.info(output.strip())
        if SPECIFIC_STRING in output:
            logging.info("Tor setup complete")
            break

    return p


def stop_tor(p):
    p.terminate()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--databaseDirectory", required=False, default="../data/",
                        help="path to database directory")
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # Alternatively: logging.basicConfig(filename=args.logFile, mode="a", level=logging.DEBUG)

    logging.info("Trying to start onion_domain harvester")
    logging.debug("Starting onion_domain harvester")

    main(args.databaseDirectory)
