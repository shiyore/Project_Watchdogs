#!/bin/bash 

#   This is the install script for setting up any tools on the raspberry pi
#
#   The install will be split into a couple different secitions
#       1. Installation of any packages
#       2. Moving of any files or directories
#       3. Anything else (setting up the database or whatever)

#imports
import os
import sys

#check that the script is run by root or someone with sudo permissions
def check_sudo():
    print("Checking if ran by sudo")

#install methods
def packages():
    print("Installing packages...")

def files():
    print("Setting up files...")

#--------------------------------------main-------------------------------------------
#print("args length: " + str(len(sys.argv)))

check_sudo()

if(len(sys.argv) > 1):
    if(str(sys.argv[1]) == "install"):
        #print("Installing")
        packages()        
        files()

    elif(str(sys.argv[1]) == "-h"):
        print("To install the project run setup.py install")

    else:
        print("ERROR: please run the program again")
        print("Usage: python3 setup.py install")

else:
    print("USAGE ERROR: please run setup.py -h for help")
