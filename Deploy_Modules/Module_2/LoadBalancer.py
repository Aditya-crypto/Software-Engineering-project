import os
import bisect
import hashlib
import socket
import random
from ConsistentHashRing import ConsistentHashRing as ConsistentHashRing



def CreateNFSList():
    with open('NFS_data.txt') as f:
        content = f.readline()
        content = content.rstrip("\n")
        nas_info = content.split(";")

    Hash_NFS = []

    for content in nas_info:
        loc_list = content.split(",")
        Hash_NFS.append(loc_list[0])

    return Hash_NFS


def hashfunc(key):
    return hash(key) % len(values)

def getItem(key):
    if(values[hashfunc(key)] is not None):
        return values[hashfunc(key)]
    else:
        return -1

def setItem(keys):
    for i in keys:
        values[hashfunc(i)] = i


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
	msg=c.recv(4096)
	print(msg)
	output = 'Thank you for connecting'
	c.sendall(output.encode('utf-8'))
	c.close()

if __name__ == "__main__":
    ## Accepting port number to start loadbalancer
    # ServerPortNumber=int(sys.argv[1])
    ## connecting part calling AcceptRequest
    keys = CreateNFSList()
    # keys.sort()
    print(keys)
    server_to_cam_mapping = {}
    consistentRing = ConsistentHashRing()
    for number in keys:
        consistentRing.add_node(number)
        server_to_cam_mapping[number] = []
    cam_sev = []
    with open('database.txt') as f:
        content = f.read().splitlines()

    # print(content)
    for i in content:
        nas_info = i.split(":")
        cam_sev.append(nas_info[0])
    # content = content.rstrip("\n")
    # nas_info = content.split(":")
    # cam_sev.append(nas_info[0])
    # print(cam_sev)

    for i in cam_sev:
        print("i: ",i)
        best_match = consistentRing.find_best_match(i)
        server_to_cam_mapping[best_match].append(i)
        print("best match: ",best_match)

    print("server_to_cam_mapping: ",server_to_cam_mapping)
    # number_to_test = random.choice(keys)
    # print("number to test: ",number_to_test)
    # best_match = consistentRingWithSignedInputs.find_best_match(number_to_test)
    # print("best match: ",best_match)
    # consistentRingWithSignedInputs.print_call()
    # setItem(keys)
    # print(values)
