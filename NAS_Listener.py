import sys
import pickle
import socket 
import os
import numpy
import threading 
from collections import deque 
import BuildMap
import CrowdDetector as CD
import time


#######################################
#INTERFACE PART
#######################################

#########################################
#MAP GENERATOR
#########################################

NearestNeighbourMap=BuildMap.NearestNeighbourMapBuilder()
ServerPortNumber=int(sys.argv[1])
CameraLocationMap=BuildMap.LocationMapBuilder()


#########################################
# MONITORING
#########################################

def conn_monitor():
    s = socket.socket()           
    ip_addr="127.0.0.1"
    port=1234
    try:
    	s.connect((ip_addr, port))
    except:
    	print("Monitor Server is not Responding !!!")
    input = 'Server at '+str(ServerPortNumber)+' is alive'
    while(True):
    	s.sendall(input.encode('utf-8'))     
    	print (s.recv(4096))
    	time.sleep(10)
    s.close()

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
    CameraLocation=CameraLocationMap[CID]
    input = 'Crowd Found in '+CameraLocation+" area"
    s.sendall(input.encode('utf-8'))     
    print (s.recv(4096)) 
    s.close()
    
########################################
# MLCROWD DETECTING ALGORITHM
########################################

CameraServerThread= threading.Thread(target=AcceptRequest,args=(), name="CameraServerThread")
CameraServerThread.start()
MonitorConnection= threading.Thread(target=conn_monitor,args=(), name="MonitorConnection")
MonitorConnection.start()

while(True):
    cameraIDList=CD.GetList()
    task=[]
    for i in range(len(cameraIDList)):
        task.append("t"+str(cameraIDList[i]))
    for i in range(len(cameraIDList)):
        task[i]= threading.Thread(target=conn,args=(cameraIDList[i],NearestNeighbourMap), name=task[i]) 
    for i in range(len(task)):
        task[i].start()
    for i in range(len(task)):
        task[i].join()
    time.sleep(10)
CameraServerThread.join() 
MonitorConnection.join()



