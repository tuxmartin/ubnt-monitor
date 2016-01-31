#!/bin/sh

echo "open $1 $2"
sleep 2
echo "POST / HTTP/1.0"
echo "User-Agent: wtf/1.0"
echo "Host: $3"
echo "Content-Type: application/json"
echo "Content-Length: 51"
echo
echo "{'id':1,'description':'TestTest','title':'Test007'}"
echo
echo
sleep 2

# JE POTREBA MIT DOBRE Content-Length !!!!!!!!!!!!!!!!!!!!!!


# ---------------------------------------------------------------

#echo "open $1 $2"
#sleep 2
#echo "GET $4 HTTP/1.0"
#echo "User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4"
#echo "Host: $3"
#echo
#echo
#sleep 2

#./getpage tonycode.com 80 tonycode.com /| telnet
#ok. what did we just do?
#getpage is sending commands on stdout and telnet is getting them via the pipe
#getpage 1st tells telnet to open a connection to tonycode.com ($1) port 80 ($2).
#getpage waits 2 seconds for the connection. Adjust as necessary.
#getpage sends the request. GET / HTTP/1.0 and sets the host ($3) to tonycode.com.
#Note $4 is the resource to fetch and we set it to /.
#I even threw in the user agent header for fun.
#Those 2 empty echo statements are necessary to tell the server this is the end of the request.
#Finally getpage sleeps for 2 seconds to allow time for the response to come back. Leave out this line and you'll get nada.
