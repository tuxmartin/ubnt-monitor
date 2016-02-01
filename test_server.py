# -*- coding: utf-8 -*-

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import json

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 9876

class Handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        message = threading.currentThread().getName()
        self.wfile.write(message)
        self.wfile.write('\n')
        return

    def do_POST(self): # Parse the form data posted
        '''
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

        if len(postvars):
            i = 0
            for key in sorted(postvars):
                print 'ARG[%d] %s=%s' % (i, key, postvars[key])
                i += 1
        '''

        content_length = int(self.headers['Content-Length'])
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


'''
Test:



    curl -v -X POST -H "Content-Type: application/json" -H "Accept: application/json" -d '{"id":1,"description":"TestTest","title":"Test007","evaluationCondition":">=","evaluationNodeAddress":12345,"evaluationValue":"11","evaluationChannel":1,"actionChannel":2,"actionNodeAddress":12345,"actionData":"22"}' http://localhost:9876



POST / HTTP/1.1
User-Agent: curl/7.35.0
Host: localhost:9876
Content-Type: application/json
Accept: application/json
Content-Length: 215

{"id":1,"description":"TestTest","title":"Test007","evaluationCondition":">=","evaluationNodeAddress":12345,"evaluationValue":"11","evaluationChannel":1,"actionChannel":2,"actionNodeAddress":12345,"actionData":"22"}HTTP/1.0 200 OK
Server: BaseHTTP/0.3 Python/2.7.6
Date: Sun, 31 Jan 2016 10:30:21 GMT

Client: ('127.0.0.1', 53279)
User-agent: curl/7.35.0
Path: /
Form data:


'''