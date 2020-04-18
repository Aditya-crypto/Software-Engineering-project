# copy code of server.py
import socket   
import signal, os    
import sounddevice as sd
import numpy as np 
from math import pi 
import sys
######################################

Serverportnumber=int(sys.argv[1])
######################################

s = socket.socket()          
print ("Socket successfully created")
port = 12346             
s.bind(('', Serverportnumber))         
print ("socket binded to %s" %(Serverportnumber))  
s.listen(5)      
print ("socket is listening") 
c, addr = s.accept()   
############################################

msg=c.recv(4096)
print(msg)
while(msg):
   fs=16000
   n=np.arange(0,3,1/fs)
   f=1000
   x=np.sin(2*pi*f*n)
   sd.play(x,fs)

output = 'Thank you for connecting'
c.sendall(output.encode('utf-8')) 

c.close() 
