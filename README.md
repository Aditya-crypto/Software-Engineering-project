# Software-Engineering-project
Police informant system to detect social gathering during covid-19 breakdown

    I. Introduction
    II. Proposed Model
    a) Formation of Distributed System
    b) Image extraction from Webcam with location(database formation)
    c) ML on images
    d) Data transmission and alert messages

# I. INTRODUCTION
    

<p align="center">
  <img src="images/model_intro.png">
</p>

<p align="center">
  <img src="images/stage1.png">
</p>
## A) Formation of Distributed System .
    
    "distributed system is a system with multiple components located on different machines that communicate and coordinate         actions in order to appear as a single coherent system to the end-user."
    In our project,the role of Ditributed System is that cameras are installed at different places and these cameras will         store the data of that place and put the stored data on the server.and the data of the server of these different places       will be sent to the server of a nearest police station,so that police will find out how many people are standing in the       crowd. If 5 or more people stand in the crowd then the police will act on them.
    
## B) Image Extraction from Webcam and storing the image in database with webcam location.

  This task needs to be done in 3 parts:\
   (i) Extracting image from webcam:\
      → Webcam will capture the video continously,so we need to extract image frames from that video stream after some        
        particular interval.This can be done using openCV and timer from time package in python.Also, we need to take care of 
        deleting/overwriting images after a particular time interval in database.\
   (ii) Fetching the location of webcam\
      → 
    
   (iii) Storing image with corresponding webcam location in the database
