#!/bin/bash
import os

#loading the file in
file = open(r"ip.txt","r+")

#i=0
for line in file:
	#print(str(i) + ". " + str(line) + "\n")
	#i += 1
	line_array = line.split()
	for i, item in enumerate(line_array):
		if(item == "inet"):
			ip_addr = line_array[i+1]
			
			#empty the ip_addr file
			ip_file = open("ip.txt", "r+")
			ip_file.truncate(0)
			ip_file.close()

			stream = os.popen("echo "+ ip_addr + " > ip.txt")
			stream.read()
file.close()
