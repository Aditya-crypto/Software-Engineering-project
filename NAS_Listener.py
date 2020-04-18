from PIL import Image
import glob
import sys
import pickle
import socket 
import os
import numpy
import threading 
from collections import deque 
################################################# 

q1 = deque()
q2 = deque()
q3 = deque()
q4 = deque()
list1=[12346,'127.0.0.1']
list2=[12341,'127.0.0.1']
list3=[12344,'127.0.0.1']
list4=[12345,'127.0.0.1']
q1.append(list1)
q2.append(list2)
q3.append(list3)
q4.append(list4)
map = {1:q1,2:q2,3:q3,4:q4}  
img_id=[1,2,3,4]
task=['t1','t2','t3','t4']
#########################################

def conn(q):
    s = socket.socket()           
    temp_list = q.popleft() 
    port=temp_list[0]  
    ip_addr=str(temp_list[1])  
    print(port)
    print(ip_addr)      
    s.connect((ip_addr, port))  
    input = 'plzz take some action'
    s.sendall(input.encode('utf-8'))     
    print (s.recv(4096)) 
    s.close()

##################################################

if __name__ == "__main__": 

    for i in range(len(img_id)):
        task[i]= threading.Thread(target=conn,args=(map[img_id[i]],), name=task[i]) 
    for i in range(len(task)):
        task[i].start()
    for i in range(len(task)):
        task[i].join()    
  
     
  