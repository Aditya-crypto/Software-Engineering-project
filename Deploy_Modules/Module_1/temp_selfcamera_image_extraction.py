#!/usr/bin/env python
# coding: utf-8

# In[19]:


import cv2
import time
import os.path
from os import path
from datetime import datetime

camera = cv2.VideoCapture(0)
serial="12345678"
for i in range(100):
    t=datetime.now()
    dirpath="UNPROCESSED/"
    if(path.exists(dirpath)):
        return_value, image = camera.read()
        print(image)
        timestamp = time.strftime('%H:%M:%S')
        hr=timestamp.split(':')
        s=str(hr[0]+'.'+hr[1]+'.'+hr[2])
        cv2.imwrite(dirpath+serial+"_"+str(s)+'.png', image)
        time.sleep(1)
    else:
        os.mkdir(dirpath)
        return_value, image = camera.read()
        timestamp = time.strftime('%H:%M:%S')
        hr=timestamp.split(':')
        s=str(hr[0]+'.'+hr[1]+'.'+hr[2])
        cv2.imwrite(dirpath+serial+"_"+str(s)+'.png', image)
        time.sleep(1)
del(camera)


# In[9]:


# import ctypes
# from primesense import openni2
# from primesense import _openni2 as c_api
# dev = openni2.Device.open_any()
# # depth_stream = dev.create_depth_stream()
# # depth_stream.start()
# # depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM, resolutionX = 320, resolutionY = 240, fps = 30))
# serial_number = str(dev.get_property(c_api.ONI_DEVICE_PROPERTY_SERIAL_NUMBER, (ctypes.c_char * 100)).value)


# In[16]:


# def getserial():
#   # Extract serial from cpuinfo file
#   cpuserial = "0000000000000000"
#   try:
#     f = open('/proc/cpuinfo','r')
#     for line in f:
        
#         if line[0:6]=='Serial':
#             cpuserial = line[10:26]
#     f.close()
#   except:
#     cpuserial = "ERROR000000000"
 
#   return cpuserial

# myserial=getserial()
# print(myserial)


# In[17]:


from pypylon import pylon 

# Pypylon get camera by serial number
serial_number = '22716154'
info = None
for i in pylon.TlFactory.GetInstance().EnumerateDevices():
    if i.GetSerialNumber() == serial_number:
        info = i
        break
else:
    print('Camera with {} serial number not found'.format(serial_number))

# VERY IMPORTANT STEP! To use Basler PyPylon OpenCV viewer you have to call .Open() method on you camera
if info is not None:
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(info))
    camera.Open()


# In[ ]:




