#!/bin/bash

echo "Ad-Hoc Network Setup"

filename='/home/pi/scoring/adhoc.txt'

while read p; do
    echo $p
    a=( $p )
    #echo ${a[0]} ${a[2]}
    sudo arp -s ${a[0]} ${a[2]}
done < $filename

exit 0
