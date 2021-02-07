#!/bin/bash python9
"""Written by Aiden Yoshioka-Miller on 02/06/21
    This is an updated version of my old script I was using to scan for nearby wireless devices. I will be updating this with any new tools I learn along the way.
    
    The goal of this script is to scan for nearby wireless APs, and hopefully nearby devices once I learn of a method to do so.
    I'm still learning about using scapy, so this is script is really basic.
"""

#imports------------------------------------------------------------------------------
from scapy.all import *
import signal 
import sys
import os

#methods------------------------------------------------------------------------------

#handling ctrl+c exit
def signal_handler(signal, frame):
    print ("Aborting program")
    os.system("kill -9 " + str(os.getpid()))
    sys.exit(1)

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

#packet sniffer 
def packet_sniffer(packet):
    try:
        source_mac = packet[0].addr2
        destination_mac = packet[0].addr1
        bssid = packet[0].addr3
    except:
        print("Cannot read MAC address")
        print(str(packet).encode("hex"))
        sys.exc_clear()

    try:
        ssid_size = packet[0][Dot11Elt].len
        ssid = packet[0][Dot11Elt].info
    except:
        ssid = ""
        ssid_size = 0

    if packet[0].type == 0:
        sub_type = packet[0][Dot11].subtype
        if str(sub_type) == "8" and ssid != "" and destination_mac.lower() == "ff:ff:ff:ff:ff:ff":
            p = packet[Dot11Elt]
            cap = packet.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}"
                                "{Dot11ProbeResp:%Dot11ProbeResp.cap%}").split('+')
            channel = None
            crypto = set()

def init_process():
    global ssid_list
    ssid_list = {}
    global s
    s = conf.L2socket(iface=new_iface)

#set wireless card to monitor mode
def monitor_mode(iface):
    print("setting " + iface + " to monitor mode...")
    os.system('ifconfig ' + iface + ' down')
    try:
        os.system("iwconfig " + iface + " mode monitor")
    except:
        print("Failed to set " + iface + " to monitor mode")
        sys.exit(1)
    os.system("ifconfig " + iface + " up")
    return iface


#main body ---------------------------------------------------------------------------------------------

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    check_syntax()
    check_sudo()
    parameters ={sys.argv[1]:sys.argv[2]}
    #print(parameters)
    if "mon" not in str(parameters["-i"]):
        new_iface = monitor_mode(parameters["-i"])
    else:
        new_iface = str(parameters["-i"])
    init_process()
    print ("sniffing on " + str(new_iface) + ".....")
    sniff(iface=new_iface, prn=packet_sniffer, store=0)
