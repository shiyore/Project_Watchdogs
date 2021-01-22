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
from colorama import Fore, Style

#check that the script is run by root or someone with sudo permissions
def check_sudo():
    #print("Checking if ran by sudo")
    if not os.geteuid() == 0:
        print("Please run as root")
        sys.exit(1)


#install methods
def packages():
    print(Fore.GREEN + "Installing packages...")
    install_string = "openssh-server apache2 libapache2-mod-wsgi-py3 python-dev"
    os.system(" apt-get install " + install_string)    

def files():
    print(Fore.GREEN + "Setting up files...")

#--------------------------------------Modules----------------------------------------
#print("args length: " + str(len(sys.argv)))
def headless_setup():
    #setting up ssh
    os.system("update-rc.d -f ssh remove")
    os.system("update-rc.d -f ssh defaults")

    #backing up ssh keys and generating new ones
    os.system("mkdir /etc/ssh/insecure_old")
    os.system("mv /etc/ssh/ssh_host* /etc/ssh/insecure_old")
    os.system("dpkg-reconfigure openssh-server")

    #enabling login without password
    read_file = open("/etc/ssh/sshd_config", "r")
    lines = read_file.readlines()
    i = 0
    for line in lines:
        if("PermitRootLogin" in line):
            lines[i] = "PermitRootLogin yes\n"
        i +=1
    
    read_file.close()
    write_file = open("/etc/ssh/sshd_config", "w")
    write_file.writelines(lines)
    write_file.close()
    
    #restarting ssh
    os.system("service ssh restart")
    os.system("update-rc.d -f ssh enable 2 3 4 5")

    #setting up autologin 
    read_file = open("/etc/lightdm/lightdm.conf", "r")
    lines = read_file.readlines()
    i = 0
    for line in lines:
        if("autologin-user=" in line):
            lines[i] = line[1:16] + "kali\n"
        i +=1
    i = 0
    for line in lines:
        if("autologin-user-timeout=" in line):
            lines[i] = line[1:]
        i +=1   
 
    read_file.close()
    write_file = open("/etc/lightdm/lightdm.conf", "w")
    write_file.writelines(lines)
    write_file.close()
    
    read_file = open("/etc/pam.d/lightdm-autologin", "r")
    lines = read_file.readlines()
    i = 0
    for line in lines:
        if("auth required pam_succeed_if.so user != root quiet_success" in line):
            lines[i] = "###" + line
        i +=1
    read_file.close()
    write_file = open("/etc/pam.d/lightdm-autologin", "w")
    write_file.writelines(lines)
    write_file.close()

def apache_setup():
    os.system("service apache2 enable & service apache2 restart")
    os.system("a2enmod wsgi")
     
#--------------------------------------main-------------------------------------------
check_sudo()

if(len(sys.argv) > 1):
    if(str(sys.argv[1]) == "install"):
        #print("Installing")
        packages()        
        files()
        apache_setup()
        headless_setup()        

    elif(str(sys.argv[1]) == "-h"):
        print("To install the project run setup.py install")

    else:
        print(Fore.RED + "ERROR: please run the program again")
        print("Usage: python3 setup.py install")

else:
    print(Fore.RED + "USAGE ERROR: please run setup.py -h for help")
