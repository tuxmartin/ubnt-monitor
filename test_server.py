from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import cgi

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

    def do_POST(self):
        # Parse the form data posted

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


        # Begin the response
        self.send_response(200)
        self.end_headers()
        self.wfile.write('Client: %s\n' % str(self.client_address))
        self.wfile.write('User-agent: %s\n' % str(self.headers['user-agent']))
        self.wfile.write('Path: %s\n' % self.path)
        self.wfile.write('Form data:\n')


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