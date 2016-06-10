# -*- coding: utf-8 -*-

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import json
import base64
import time



SERVER_HOST = "0.0.0.0"
SERVER_PORT = 9876

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

        firmware = data['status']['firmware']['version']
        uptime = data['status']['host']['uptime']

        for x in data['ifstats']['interfaces']:
            if x['ifname'] == 'ath0':
                ath0_rx_bytes = x['stats']['rx_bytes']
            elif x['ifname'] == 'eth0':
                eth0_tx_bytes = x['stats']['tx_bytes']

        for y in data['iflist']['interfaces']:
            if y['ifname'] == 'ath0':
                mode = y['wireless']['mode']
                channel = y['wireless']['channel']
                signal = y['wireless']['signal']
                essid = y['wireless']['essid']
                txrate = y['wireless']['txrate']
                rxrate = y['wireless']['rxrate']

                airmax = y['wireless']['polling']['enabled']
                airmax_quality = y['wireless']['polling']['quality']
                airmax_capacity = y['wireless']['polling']['capacity']

            if y['ifname'] == 'br0':
                ipv4_addr = y['ipv4']['addr']
                ipv4_netmask = y['ipv4']['netmask']

        print(time.strftime("%d-%m-%Y %H:%M:%S"))
        print "Prijata data: " \
              "\n\t firmware= %s " \
              "\n\t uptime= %s " \
              "\n\t eth0 tx bytes= %s " \
              "\n\t eth0 ipv4= %s / %s " \
              "\n\t ath0 rx bytes= %s " \
              "\n\t ath0 mode= %s " \
              "\n\t ath0 channel= %s " \
              "\n\t ath0 signal= %s " \
              "\n\t ath0 essid= %s " \
              "\n\t ath0 txrate= %s " \
              "\n\t ath0 rxrate= %s " \
              "\n\t ath0 airmax= %s " \
              "\n\t ath0 airmax_quality= %s " \
              "\n\t ath0 airmax_capacity= %s " \
              % (firmware, uptime, eth0_tx_bytes, ipv4_addr, ipv4_netmask, ath0_rx_bytes,
                 mode, channel, signal, essid, txrate, rxrate, airmax, airmax_quality, airmax_capacity)

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
