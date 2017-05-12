#!/bin/bash

PEERNR=$1
AP=$2

echo "Setting Up Network Chain for:" $PEERNR

if [ $PEERNR = 1 ]; then
	echo "192.168.4.2"
	sudo arp -s 192.168.4.2 b8:27:eb:7f:8c:f3
fi

if [ $PEERNR = 2 ]; then
        echo "192.168.4.1"
        sudo arp -s 192.168.4.1 b8:27:eb:78:6f:4d
	echo "192.168.4.3"
	sudo arp -s 192.168.4.3 b8:27:eb:36:6d:37
fi

if [ $PEERNR = 3 ]; then
        echo "192.168.4.2"
	sudo arp -s 192.168.4.2 b8:27:eb:7f:8c:f3
	echo "192.168.4.4"
	sudo arp -s 192.168.4.4 b8:27:eb:3c:dc:97
fi

if [ $PEERNR = 4 ]; then
        echo "192.168.4.3"
        sudo arp -s 192.168.4.3 b8:27:eb:36:6d:37
fi

if [ $PEERNR = "all" ]; then
        echo "All"
        /bin/bash ./adhocsetup.sh

fi

echo "Starting Docker"

docker-compose up -d --build

if [ $AP = "AP" ]; then
	echo "Setting up firewall for AP"
	IP=$(docker inspect -f '{{ .NetworkSettings.Networks.scoring_default.IPAddress }}' scoring_website_1)
	echo $IP
#	echo "Deleting old rule if any..."
#	sudo iptables -D DOCKER ! -d $IP -i wlan1 -j DROP
#	sudo iptables -D DOCKER -d $IP -m iprange --src-range 192.168.42.10-192.168.42.200 -j DROP
	echo "Insert new rule..."
	sudo iptables -I DOCKER ! -d $IP -i wlan1 -j DROP
#	sudo iptables -I DOCKER -d $IP -i wlan1 -j DROP
#	sudo iptables -I DOCKER -d $IP -m iprange --src-range 192.168.42.10-192.168.42.200 -j DROP
fi

echo "** Setup Chain Done **"

exit 0
