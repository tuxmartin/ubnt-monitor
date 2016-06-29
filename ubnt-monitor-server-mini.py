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

        pppoe_username = data['pppoe']['username']

        for x in data['iflist']['interfaces']: # IPv6
            if x['ifname'] == 'br0':
                if 'ipv6' in x :
                    for y in x['ipv6']:
                        if y['addr'].startswith('2001'): # doplnit podle IPv6
                            ipv6_addr = y['addr']
                            ipv6_plen = y['plen']
            if x['ifname'] == 'eth0':
                if 'ipv6' in x:
                    for y in x['ipv6']:
                        if y['addr'].startswith('2001'): # doplnit podle IPv6
                            ipv6_addr = y['addr']
                            ipv6_plen = y['plen']

        to_syslog += "pppoe_username='" + str(pppoe_username) + "';"

        print(time.strftime("%d-%m-%Y %H:%M:%S"))
        print "Prijata data: " \
              "\n\t 'pppoe_username=%s' " \
              % (pppoe_username)

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
