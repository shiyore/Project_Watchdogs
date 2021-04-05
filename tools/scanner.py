"""
Written by Aiden Yoshioka-Miller on 01/06/21

I'm still learning how to use scapy, so this is still very basic. Some of the code is following a demonstration: 
https://www.thepythoncode.com/article/building-wifi-scanner-in-python-scapy
"""

#imports------------------------------------------------------------------------------------
from scapy.all import *
from threading import Thread
import os
import signal
import time
import pandas

#methods-------------------------------------------------------------------------------------

#initializing dataframes
networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel" , "Crypto"])
networks.set_index("BSSID" , inplace=True)

def callback(packet):
    if packet.haslayer(Dot11Beacon):
        #getting the mac
        bssid = packet[Dot11].addr2
        #getting the ssid
        ssid = packet[Dot11Elt].info.decode()

        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
        #get network stats
        stats = packet[Dot11Beacon].network_stats()
        #get channel of AP
        channel = stats.get("channel")
        #get crypto
        crypto = stats.get("crypto")
        networks.loc[bssid] = (ssid, dbm_signal , channel , crypto)

#function to print the currently scanned networks
def write_results(network):
    file1 = open("scan_results.txt", "w")  # append mode 
    file1.write(str(network) + " \n") 
    file1.close() 

#printing function
def print_all():
    time_end = time.time() + 4.5
    while time.time() < time_end:
        os.system("clear")
        print(networks)
        write_results(networks)
        time.sleep(0.5)
    os.system("kill -9 " + str(os.getpid()))
    sys.exit()

#channel changer
def change_channel():
    ch = 1
    while True:
        os.system(f"iwconfig {interface} channel {ch}")
        ch = ch % 14 + 1
        time.sleep(0.5)

#check if ran with root permissions
def check_sudo():
    if not os.getuid() == 0:
        print("Please run with root privelages")
        sys.exit(1)
#check for correct syntax    
def check_syntax():
    if len(sys.argv) < 3:
        print("Syntax Error: \n Usage: python3 scanner.py -i <interface>")
        sys.exit(1)
# start the channel changer
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()
#handling ctrl_c exit
def signal_handler(signal, frame):
    print ("\nAborting program")
    os.system("kill -9 " + str(os.getpid()))
    sys.exit(1)

#main-----------------------------------------------------------------------------------------

if __name__ == "__main__":
    check_sudo()
    check_syntax()
    #checking interface
    parameters ={sys.argv[1]:sys.argv[2]}
    interface = parameters["-i"]
    #start thread to print all devices
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()
    # start the channel changer
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start() 
    #start sniffing for packets
    sniff(prn=callback , iface=interface)
