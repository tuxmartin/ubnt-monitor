#!/bin/sh

IP="77.88.90.200"

PORT="9876"
INTERVAL=60

while true; do
  /etc/persistent/ubnt-monitor.sh | telnet $IP $PORT
  sleep $INTERVAL
done
