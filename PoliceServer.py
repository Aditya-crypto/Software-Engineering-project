import socket   
import signal, os    
import sounddevice as sd
import numpy as np 
from math import pi 
import sys


Serverportnumber=int(sys.argv[1])


CreateSocket = socket.socket()          
print ("Socket successfully created")       
CreateSocket.bind(('', Serverportnumber))         
print ("socket binded to %s" %(Serverportnumber))  
CreateSocket.listen(5)      
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

