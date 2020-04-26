import socket   
import signal, os    
import sounddevice as sd
import numpy as np 
from math import pi 
import sys
import threading
import time

######################################
ServerportNumber=int(sys.argv[1])
######################################

#########################################
# MONITORING
#########################################

def conn_monitor():
    s = socket.socket()           
    ip_addr="127.0.0.1"
    port=1234
    try:
    	s.connect((ip_addr, port))
    	print("connected")
    except:
    	print("Monitor Server is not Responding !!!")
    
    while(True):
    	input = 'Server at '+str(ServerportNumber)+' is alive '
    	try:
    		s.sendall(input.encode('utf-8'))
    		time.sleep(10)
    	except:
    		print("send nothing")
    s.close()

############################################
# SEND ALERT
############################################


def alert():
	s = socket.socket()          
	print ("Socket successfully created")           
	s.bind(('', ServerportNumber))         
	print ("socket binded to %s" %(ServerportNumber))  
	s.listen(5)      
	print ("socket is listening")
	while(True):
		c, addr = s.accept()
		msg=c.recv(4096)
		print(msg)
		while(msg):
			fs=16000
			n=np.arange(0,3,1/fs)
			f=1000
			x=np.sin(2*pi*f*n)
			sd.play(x,fs)
		output = 'Thank you for Information'
		c.sendall(output.encode('utf-8')) 
		c.close()
############################################
# MULTITHREADING
############################################

MonitorConn= threading.Thread(target=conn_monitor,args=(), name="MonitorConn")
MonitorConn.start()
recvalert= threading.Thread(target=alert,args=(), name="recvalert")
recvalert.start()
MonitorConn.join()
recvalert.join()
