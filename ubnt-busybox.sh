#!/bin/sh
# funguje s busybox telnetem i s normalnim telnetem v ubuntu

#  ./ubnt-busybox.sh | telnet 10.123.1.11 9876

echo "POST / HTTP/1.0"
echo "User-Agent: wtf/1.0"
echo "Content-Type: application/json"
echo "Content-Length: 51"
echo
echo '{"id":1,"description":"TestTest","title":"Test007"}'
echo
echo

# JE POTREBA MIT DOBRE Content-Length !!!!!!!!!!!!!!!!!!!!!!
