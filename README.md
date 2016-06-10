## Ukazka:

https://youtu.be/PZYKfAn_ex8

Data ze zarizeni je mozne posilat jako plain text, nebo gzip-base64.

Neni mozne poslat samotny gzip, protoze telent client v binarni stremu zacne vyhodnocovat ridici znaky a spadne. Proto se gzip pred odeslanim prevede na base64.

Serverova cast v Pythonu sama detekuje, zda je vstup plain text, nebo base64/gzip.

**Pro srovnani: cisty text zaberal pri testovani 10580 bajtu a base64-gzip 3056 bajtu - 3,46x mene.**

## Ukazkovy vystup:
```
/usr/bin/python2.7 /home/martin/PycharmProjects/ubnt-monitor/test_server.py
Starting server, use <Ctrl-C> to stop
10.123.66.3 - - [01/Feb/2016 20:56:43] "POST / HTTP/1.0" 200 -
{ "status": {"version":1,"device":{"id":"44d9e75d52fe","system_id":59413,"revision":0},"board":{"system_id":5941 ...

Prijata data:
	 firmware= XW.ar934x.v5.6.3.28591.151130.1735
	 uptime= 3563
	 eth0 tx bytes= 2355109
	 eth0 ipv4= 10.123.66.3 / 255.255.255.0
	 ath0 rx bytes= 288233
	 ath0 mode= ap
	 ath0 channel= 104
	 ath0 signal= -51
	 ath0 essid= MV_1
	 ath0 txrate= 130.0
	 ath0 rxrate= 130.0
	 ath0 airmax= 1
	 ath0 airmax_quality= 95
	 ath0 airmax_capacity= 89

```	 

# Instalace

## Stazeni
Nakopirovat soubor `ubnt-monitor.sh` do `/etc/persistent/ubnt-monitor.sh` a nastavit mu prava spusteni a ulozit:

```
lokalPC$ scp ubnt-monitor.sh admin@1.2.3.4:/etc/persistent
```

```
chmod a+x /etc/persistent/ubnt-monitor.sh
save
```

## Automaticke spusteni kazdou minutu

V UBNT je "divny" cron. Podle prispevku na foru viz soubor `doc/ubnt_cron.txt` by mel fungovat, ale nefunguje.
Proto jsem pouzil while-true loop.

Do `/etc/persistent/rc.poststart` pridat:

```bash
while true; do
  /etc/persistent/ubnt-monitor.sh | telnet 10.20.30.40 9876
  sleep 60
done &
```
TODO: cyklus se nesposti, opravit!

Kde `10.20.30.40 9876` je IP a port serveru, na ktery se posilaji data.

A nakonec ulozit a restartovat zarizeni:

```bash
save
reboot
```
