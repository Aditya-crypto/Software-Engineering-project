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

# B) Image Extraction from Webcam and storing the image in database with webcam location.

  This task needs to be done in 3 parts:\
   (i) Extracting image from webcam:\
      → Webcam will capture the video continously,so we need to extract image frames from that video stream after some        
        particular interval.This can be done using openCV and timer from time package in python.Also, we need to take care of 
        deleting/overwriting images after a particular time interval in database.\
   (ii) Fetching the location of webcam\
      → 
    
   (iii) Storing image with corresponding webcam location in the database
