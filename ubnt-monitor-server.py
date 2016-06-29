# -*- coding: utf-8 -*-

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import json
import base64
import time

# syslog:
import logging
import logging.handlers


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 9876

# syslog:
my_logger = logging.getLogger('UBNT-MONITOR')
my_logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address = '/dev/log')

my_logger.addHandler(handler)
class Handler(BaseHTTPRequestHandler):

    def gzipDecode(self, content):
        import StringIO
        import gzip

        outFile = StringIO.StringIO()

        compressedFile = StringIO.StringIO(content)
        decompressedFile = gzip.GzipFile(fileobj=compressedFile)

        outFile.write(decompressedFile.read())
        outFile.flush()
        outFile.seek(0) # You need to seek back to the start before you can read.

        return outFile.read().replace('\n', '')

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        message = threading.currentThread().getName()
        self.wfile.write(message)
        self.wfile.write('\n')
        return

    def do_POST(self): # Parse the form data posted
        to_syslog = "UBNT-MONITOR "
        file_content = ''
        content_length = int(self.headers['Content-Length'])
        print "Content-Length=" + str(content_length)

        if (
            'Content-Encoding' in self.headers and
            'Content-Transfer-Encoding' in self.headers and
            self.headers['Content-Encoding'.lower()] == 'gzip' and
            self.headers['Content-Transfer-Encoding'.lower()] == 'base64'
        ):
            print "___BASE64-GZIP"
            compressedData = self.rfile.read(content_length)
            file_content = self.gzipDecode(base64.b64decode(compressedData))
        else:
            print "___PLAIN-TEXT"
            file_content = self.rfile.read(content_length)

        print file_content

        # https://pythonspot.com/json-encoding-and-decoding-with-python/
        data = json.loads(file_content)

        firmware = data['board_info']['firmware']
        board_shortname = data['board_info']['board_shortname']

        pppoe_username = data['pppoe']['username']

        uptime = data['status']['host']['uptime']

        for x in data['status']['interfaces']:
            if x['ifname'] == 'ath0':
                signal = x['wireless']['signal']
                rssi = x['wireless']['rssi']
                noisef = x['wireless']['noisef']
                ccq = x['wireless']['ccq']
                txrate = x['wireless']['txrate']
                rxrate = x['wireless']['rxrate']

                if x['wireless']['polling']['quality']:  # N zarizeni
                    airmax_quality = x['wireless']['polling']['quality']
                    airmax_capacity = x['wireless']['polling']['capacity']

        for x in data['ifstats']['interfaces']:
            if x['ifname'] == 'ath0':
                rx_bytes = x['stats']['rx_bytes']
                tx_bytes = x['stats']['tx_bytes']

        for x in data['status']['interfaces']: # IPv4
            if x['ifname'] == 'br0':
                if x['ipv4']:
                    ipv4_addr = x['ipv4']['addr']
                    ipv4_netmask = x['ipv4']['netmask']
                    ipv4_broadcast = x['ipv4']['broadcast']

        for x in data['iflist']['interfaces']: # IPv6
            if x['ifname'] == 'br0':
                if x['ipv6']:
                    for y in x['ipv6']:
                        if y['addr'].startswith('2001'): # doplnit podle IPv6
                            ipv6_addr = y['addr']
                            ipv6_plen = y['plen']
            if x['ifname'] == 'eth0':
                if x['ipv6']:
                    for y in x['ipv6']:
                        if y['addr'].startswith('2001'): # doplnit podle IPv6
                            ipv6_addr = y['addr']
                            ipv6_plen = y['plen']

        to_syslog += "firmware='" + str(firmware) + "';"
        to_syslog += "board_shortname='" + str(board_shortname) + "';"
        to_syslog += "pppoe_username='" + str(pppoe_username) + "';"
        to_syslog += "uptime='" + str(uptime) + "';"
        to_syslog += "ath0_signal='" + str(signal) + "';"
        to_syslog += "ath0_rssi='" + str(rssi) + "';"
        to_syslog += "ath0_noisef='" + str(noisef) + "';"
        to_syslog += "ath0_ccq='" + str(ccq) + "';"
        to_syslog += "ath0_txrate='" + str(txrate) + "';"
        to_syslog += "ath0_rxrate='" + str(rxrate) + "';"
        to_syslog += "ath0_rx_bytes='" + str(rx_bytes) + "';"
        to_syslog += "ath0_tx_bytes='" + str(tx_bytes) + "';"
        to_syslog += "br0_ipv4_addr='" + str(ipv4_addr) + "';"
        to_syslog += "br0_ipv4_netmask='" + str(ipv4_netmask) + "';"
        to_syslog += "br0_ipv4_broadcast='" + str(ipv4_broadcast) + "';"

        print(time.strftime("%d-%m-%Y %H:%M:%S"))
        print "Prijata data: " \
              "\n\t 'firmware=%s' " \
              "\n\t 'board_shortname=%s' " \
              "\n\t 'pppoe_username=%s' " \
              "\n\t 'uptime=%s' " \
              "\n\t 'ath0_signal=%s' " \
              "\n\t 'ath0_rssi=%s' " \
              "\n\t 'ath0_noisef=%s' " \
              "\n\t 'ath0_ccq=%s' " \
              "\n\t 'ath0_txrate=%s' " \
              "\n\t 'ath0_rxrate=%s' " \
              "\n\t 'ath0_rx_bytes=%s' " \
              "\n\t 'ath0_tx_bytes=%s' " \
              "\n\t 'br0_ipv4_addr=%s' " \
              "\n\t 'br0_ipv4_netmask=%s' " \
              "\n\t 'br0_ipv4_broadcast=%s' " \
              % (firmware, board_shortname, pppoe_username, uptime, signal, rssi, noisef, ccq, txrate, rxrate, rx_bytes, tx_bytes, ipv4_addr, ipv4_netmask, ipv4_broadcast)

        if airmax_quality and airmax_capacity:
            to_syslog += "ath0_airmax_quality='" + str(airmax_quality) + "';"
            to_syslog += "ath0_airmax_capacity='" + str(airmax_capacity) + "';"
            print "\n\t 'ath0_airmax_quality=%s' " \
                  "\n\t 'ath0_airmax_capacity=%s' " \
                  % (airmax_quality, airmax_capacity)

        if ipv6_addr and ipv6_plen:
            to_syslog += "br0_ipv6_addr='" + str(ipv6_addr) + "';"
            to_syslog += "br0_ipv6_plen='" + str(ipv6_plen) + "';"
            print "\n\t 'br0_ipv6_addr=%s' " \
                  "\n\t 'br0_ipv6_plen=%s' " \
                  % (ipv6_addr, ipv6_plen)


        print to_syslog
        my_logger.info(to_syslog)

        # Begin the response
        self.send_response(200)
        self.send_header("Connection", "close")
        self.end_headers()
        #self.wfile.write('Client: %s\n' % str(self.client_address))

        print ""
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer((SERVER_HOST, SERVER_PORT), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
