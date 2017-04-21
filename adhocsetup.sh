#!/bin/bash

echo "Ad-Hoc Network Setup"

filename='/home/pi/scoring/adhoc.txt'

while read p; do
    echo $p
    sudo arp -s $p
done < $filename

exit 0
