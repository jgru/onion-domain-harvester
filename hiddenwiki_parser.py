__author__ = 'gru'

import socks
import socket



from domain_harvester import HtmlHarvester



if __name__ == "__main__":
    url = 'http://icanhazip.com/'

    htmlHarvester = HtmlHarvester(url, None, None)
    html = htmlHarvester.load_page()
    print('ip: {}'.format(html.strip()))

    socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
    socket.socket = socks.socksocket
    # socks.set_proxy(socks.SOCKS5, "localhost", "9050'")
    htmlHarvester = HtmlHarvester(url, None, None)
    html = htmlHarvester.load_page()
    print('ip: {}'.format(html.strip()))


