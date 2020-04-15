from PIL import Image
import glob
import sys
import pickle
import socket 
import os
import numpy
from collections import deque 
   
q = deque()
list=[12346,'127.0.0.1']
q.append(list)
map = {1: q}  
img_id=1

#########################################
s = socket.socket()           
temp_list = map[img_id].popleft() 
port=temp_list[0]  
ip_addr=str(temp_list[1])  
print(port)
print(ip_addr)      
s.connect((ip_addr, port))  
#######################################


input = 'plzz take some action'
s.sendall(input.encode('utf-8'))     
print (s.recv(4096)) 
s.close()   