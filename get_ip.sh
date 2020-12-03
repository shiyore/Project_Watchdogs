#!/bin/zsh

FILE=ip.txt
if test -f "$FILE";then
	sudo rm -r ip.txt
fi
sudo ifconfig wlp1s0 >> ip.txt &

sudo python3 parse_ip.py

cat ip.txt | telegram-send --stdin

