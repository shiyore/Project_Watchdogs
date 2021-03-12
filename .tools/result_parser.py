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
import pickle

#methods-------------------------------------------------------------------------------------
def read_file(file_name):
        fileObj = open(file_name, "r") #opens the file in read mode
        words = fileObj.read().splitlines() #puts the file into an array
        fileObj.close()
        return words

def parse_results():
    devices = []
    lines = read_file("scan_results.txt")
    for line in lines[2:]:
        if len(line.split()) >= 5:
            line_arr = line.split()
            devices.append({"name": line_arr[1] if line_arr[1] != '\x00' else 'hidden' , "mac": line_arr[0], "channel": line_arr[3], "encryption": line_arr[4]})
    return devices
#main-----------------------------------------------------------------------------------------

if __name__ == "__main__":
    with open('results.pkl', 'wb') as fp:
        pickle.dump(parse_results(), fp)