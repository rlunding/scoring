#!/bin/bash

PEERNR=$1

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

exit 0
