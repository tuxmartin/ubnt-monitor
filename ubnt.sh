#!/bin/sh
# funguje s busybox telnetem i s normalnim telnetem v ubuntu

#  ./ubnt.sh | telnet 10.123.1.11 9876

TMP=`mktemp -t`

FIRMWARE=`cat /etc/version | tr "\\n" " " | sed 's/.$//'`
BOARD_NAME=`cat /etc/board.info | grep "board.name" | sed 's/board.name=//' | tr "\\n" " " |  sed 's/.$//'`
BOARD_SHORTNAME=`cat /etc/board.info | grep "board.shortname" | sed 's/board.shortname=//' | tr "\\n" " " |  sed 's/.$//'`

echo '{ "board_info": {'  > $TMP
echo ' "firmware": "'$FIRMWARE'",'  >> $TMP
echo ' "board_name": "'$BOARD_NAME'",'  >> $TMP
echo ' "board_shortname": "'$BOARD_SHORTNAME'"},'  >> $TMP

echo '"status": '  >> $TMP
ubntbox status >> $TMP
echo ', "ifstats":' >> $TMP
ubntbox ifstats.cgi | tail -n +3 | tr "\\n" " " | tr -s '\t' ' ' | sed 's/.$//'  >> $TMP
echo ',"iflist":' >> $TMP
ubntbox iflist.cgi | tail -n +3 | tr "\\n" " " | tr -s '\t' ' ' | sed 's/.$//'  >> $TMP
echo '}' >> $TMP

LENGTH=`cat $TMP | wc -c` # JE POTREBA MIT DOBRE Content-Length !

echo "POST / HTTP/1.0"
echo "User-Agent: wtf/1.0"
echo "Content-Type: application/json"
echo "Cache-Control: no-cache"
echo "Pragma: no-cache"
echo "Connection: close"
echo "Content-Length: $LENGTH"
echo
echo `cat $TMP`
echo

rm $TMP
