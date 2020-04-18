import sys
import pickle
import socket 
import os
from collections import deque 
import sys

#######################################
#INTERFACE PART
#######################################

CreateSocket = socket.socket()
Serverportnumber=int(sys.argv[1])

#######################################

NumberOfNASservers=5
SequenceNumber=Serverportnumber%NumberOfNASservers

########################################
#CONNECTING TO NAS
########################################
NASport,NASIPAddr=NASServerlist[SequenceNumber]
NASport=int(NASport)
NASIPAddr=str(NASIPAddr)
CreateSocket.connect((NASIPAddr,NASport))

input = 'I want To Connect'
CreateSocket.sendall(input.encode('utf-8'))

ack=CreateSocket.recv(4096)
print(ack)

#############################################
#MOUNTING PART OF NAS
############################################
#while(ack):
#	os.mkdir("foldername")
	#code for mounting

##############################################
#CAMERA TAKING IMAGES
##############################################
