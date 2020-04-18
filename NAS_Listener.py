import sys
import pickle
import socket 
import os
import numpy
import threading 
from collections import deque 
import BuildMap
#import Crowddetector as CD

#########################################
#MAP GENERATOR
#########################################

NearestNeighbourMap=buildmap.MapBuilder()
ServerPortNumber=int(sys.argv[1])

#########################################
# ACCEPT REQUEST
#########################################


def AcceptRequest():
	s = socket.socket()          
	print ("Socket successfully created")           
	s.bind(('', ServerPortnumber))         
	print ("socket binded to %s" %(ServerPortNumber))  
	s.listen(5)      
	print ("socket is listening") 
	c, addr = s.accept()
	#MOUNTING PART
	msg=c.recv(4096)
	print(msg)
	output = 'Thank you for connecting'
	c.sendall(output.encode('utf-8'))
	c.close() 


########################################
# MLCROWD DETECTING ALGORITHM
########################################

cameraIDList=CD.FindCID()
# img_id=[1,2,3,4]
task=['t1','t2','t3','t4']

#########################################
# REPORTING TO NEAREST POLICE SERVER
#########################################
def conn(CID,NearestNeighbourMap):
    s = socket.socket()           
    temp_list = NearestNeighbourMap[CID]
    port,ip_addr=temp_list[0].split(',')
	ip_addr=str(ip_addr)
	port=int(port)     
    s.connect((ip_addr, port))  
    input = 'plzz take some action'
    s.sendall(input.encode('utf-8'))     
    print (s.recv(4096)) 
    s.close()
    
########################################
# MULTITHREADING
########################################

if __name__ == "__main__": 
    
    CameraServerThread= threading.Thread(target=AcceptRequest,args=(), name=CameraServerThread)
	CameraServerThread.start()
    for i in range(len(img_id)):
        task[i]= threading.Thread(target=conn,args=(cameraIDList[i],NearestNeighbourMap), name=task[i]) 
    for i in range(len(task)):
        task[i].start()
    for i in range(len(task)):
        task[i].join()    
  





     
  
