import sys
import pickle
import socket 
import os
import numpy
import threading 
from collections import deque 
import BuildMap as buildmap
import time


N=4 #number of total servers 

ServerPortNumber=int(sys.argv[1])
def monitor_server(c):
	while(True):
		try:
			msg=c.recv(24)
			print(msg,flush=True)
		except:
			print("nothing recieved")



s = socket.socket()          
# print ("Socket successfully created")     
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      
s.bind(('', ServerPortNumber))         
# print ("socket binded to %s" %(ServerPortNumber))  
s.listen(5)      
print ("socket is listening")
task=[]
for i in range(N):
	task.append("t"+str(i))
k=0
while(True):
	c, addr = s.accept()
	task[k]= threading.Thread(target=monitor_server,args=[c], name=task[k])
	task[k].start()
	k+=1





